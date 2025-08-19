import os
from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SavingsGroup, SavingsMember, Transaction
from django.contrib.auth.models import User
from django.db.models import Sum

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

