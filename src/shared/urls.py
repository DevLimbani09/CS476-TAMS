from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "shared"

urlpatterns = [
    path("dashboard.html", views.dashboard_view, name="dashboard"),
    path("notifications.html", views.notifications_view, name="notifications"),
    path(
        "notification_details.html",
        views.notification_details_view,
        name="notification_details_default",
    ),
    path(
        "notification_details/<int:pk>/",
        views.notification_details_view,
        name="notification_details",
    ),
    path("profile.html", views.profile_view, name="profile"),
    path("edit_profile.html", views.edit_profile_view, name="edit_profile"),
    path("settings.html", views.settings_view, name="settings"),
    path("help_support.html", views.help_support_view, name="help_support"),
]

# Legacy admin template path aliases redirected to the shared namespace
urlpatterns += [
    path(
        "templates/notifications.html",
        RedirectView.as_view(pattern_name="shared:notifications", permanent=False),
    ),
    path(
        "templates/profile.html",
        RedirectView.as_view(pattern_name="shared:profile", permanent=False),
    ),
    path(
        "templates/settings.html",
        RedirectView.as_view(pattern_name="shared:settings", permanent=False),
    ),
    path(
        "templates/help_support.html",
        RedirectView.as_view(pattern_name="shared:help_support", permanent=False),
    ),
]