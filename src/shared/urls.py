from django.urls import path
from . import views

app_name = "shared"

urlpatterns = [
    path("dashboard.html", views.dashboard_view, name="dashboard"),
    path("notifications.html", views.notifications_view, name="notifications"),
    path("notification_details.html", views.notification_details_view, name="notification_details_default"),
    path("notification_details/<int:pk>/", views.notification_details_view, name="notification_details"),
    path("profile.html", views.profile_view, name="profile"),
    path("edit_profile.html", views.edit_profile_view, name="edit_profile"),
    path("settings.html", views.settings_view, name="settings"),
    path("help_support.html", views.help_support_view, name="help_support"),
]