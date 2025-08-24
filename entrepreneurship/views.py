import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SavingsGroup, SavingsMember, Transaction
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MentorProfile, MentorshipRequest
from django.core.mail import send_mail

def mentor_directory(request):
    skills = request.GET.get("skills")
    availability = request.GET.get("availability")

    mentors = MentorProfile.objects.all()
    if skills:
        mentors = mentors.filter(skills__icontains=skills)
    if availability:
        mentors = mentors.filter(availability=True)

    return render(request, "mentors/directory.html", {"mentors": mentors})


@login_required
def savings_dashboard(request):
    groups = SavingsGroup.objects.all()
    return render(request, "entrepreneurship/savings_dashboard.html", {"groups": groups})


@login_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        group = SavingsGroup.objects.create(name=name)
        SavingsMember.objects.create(user=request.user, group=group, balance=0)
        return redirect("savings_dashboard")
    return render(request, "entrepreneurship/create_group.html")


@login_required
def join_group(request, group_id):
    group = get_object_or_404(SavingsGroup, id=group_id)
    SavingsMember.objects.get_or_create(user=request.user, group=group, balance=0)
    return redirect("group_detail", group_id=group.id)


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(SavingsGroup, id=group_id)
    members = SavingsMember.objects.filter(group=group)
    transactions = Transaction.objects.filter(group=group).order_by("-date")
    return render(request, "entrepreneurship/group_detail.html", {
        "group": group,
        "members": members,
        "transactions": transactions
    })


@login_required
def make_transaction(request, group_id):
    group = get_object_or_404(SavingsGroup, id=group_id)
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        member = SavingsMember.objects.get(user=request.user, group=group)
        member.balance += amount
        member.save()

        group.total_balance = SavingsMember.objects.filter(group=group).aggregate(Sum("balance"))["balance__sum"] or 0
        group.save()

        Transaction.objects.create(user=request.user, group=group, amount=amount)
        return redirect("group_detail", group_id=group.id)
    return render(request, "entrepreneurship/transaction.html", {"group": group})


def download_template(request, template_name):
    file_path = os.path.join(settings.BASE_DIR, "entrepreneurship", "static", "files", f"{template_name}.pdf")
    if not os.path.exists(file_path):
        raise Http404("Template not found")
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required
def send_request(request, mentor_id):
    mentor = get_object_or_404(MentorProfile, id=mentor_id)

    if request.method == "POST":
        message = request.POST.get("message")
        MentorshipRequest.objects.create(
            mentee=request.user,
            mentor=mentor.user,
            message=message
        )
        # Notify mentor
        send_mail(
            subject=f"New Mentorship Request from {request.user.username}",
            message="Log in to review the request.",
            from_email="admin@sheworks.com",
            recipient_list=[mentor.user.email],
        )
        return redirect("mentor_directory")

    return render(request, "mentors/request_form.html", {"mentor": mentor})
@login_required
def mentor_requests(request):
    requests = request.user.received_requests.all()
    return render(request, "mentors/dashboard.html", {"requests": requests})


@login_required
def handle_request(request, request_id, action):
    req = get_object_or_404(MentorshipRequest, id=request_id, mentor=request.user)

    if action == "accept":
        req.status = "Accepted"
        send_mail(
            f"Your request was accepted by {request.user.username}",
            "Congratulations! Your mentor has accepted your request.",
            "admin@sheworks.com",
            [req.mentee.email],
        )
    elif action == "reject":
        req.status = "Rejected"
        send_mail(
            f"Your request was rejected by {request.user.username}",
            "Unfortunately, your mentor has rejected your request.",
            "admin@sheworks.com",
            [req.mentee.email],
        )
    req.save()
    return redirect("mentor_requests")
