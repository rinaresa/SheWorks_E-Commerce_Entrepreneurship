from django.urls import path
from . import views

urlpatterns = [
    # Business Templates
    path("tools/business-templates/<str:template_name>/", views.download_template, name="download_template"),
    path("tools/", views.savings_dashboard, name="savings_dashboard"),

    # Savings Groups
    path("savings/groups/", views.savings_dashboard, name="savings_dashboard"),
    path("savings/groups/create/", views.create_group, name="create_group"),
    path("savings/groups/<int:group_id>/join/", views.join_group, name="join_group"),
    path("savings/groups/<int:group_id>/", views.group_detail, name="group_detail"),
    path("savings/groups/<int:group_id>/transactions/", views.make_transaction, name="make_transaction"),

    path("mentors/", views.mentor_directory, name="mentor_directory"),
    path("mentors/<int:mentor_id>/request/", views.send_request, name="send_request"),
    path("mentors/requests/", views.mentor_requests, name="mentor_requests"),
    path("mentors/requests/<int:request_id>/<str:action>/", views.handle_request, name="handle_request"),

]
