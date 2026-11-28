from types import SimpleNamespace

from authentication.access import account_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render

from .models import Notification

User = get_user_model()


def ensure_profile(user):
    """Build a lightweight profile view-model from the custom User attributes."""
    return SimpleNamespace(
        user=user,
        employee_id=str(user.employee_id),
        preferred_name=user.get_full_name(),
        contact_number=user.contact_number or "",
        department="",
        manager=user.manager,
        account_status="Active" if user.account_status else "Inactive",
    )


@account_required
def dashboard_view(request):
    """Redirect users to the role-aware dashboard route."""
    return redirect("dashboard")


@account_required
def notifications_view(request):
    """List the logged-in user's notifications with optional status and type filters."""
    qs = Notification.objects.filter(user=request.user)
    unread = qs.filter(is_read=False).count()
    status = request.GET.get("read_status", "all")
    kind = request.GET.get("notification_type", "all")

    # Apply read/unread filter if requested
    if status == "read":
        qs = qs.filter(is_read=True)
    elif status == "unread":
        qs = qs.filter(is_read=False)

    # Apply category filter if it matches a valid notification type
    if kind in dict(Notification.TYPE_CHOICES):
        qs = qs.filter(notification_type=kind)

    return render(
        request,
        "shared/notifications.html",
        {
            "notifications": qs[:100],
            "unread_count": unread,
            "selected_read_status": status,
            "selected_notification_type": kind,
        },
    )


@account_required
def notification_details_view(request, pk=None):
    """Display a single notification and allow the recipient to mark it as read."""
    notification_id = pk or request.GET.get("id")

    # Redirect back to the inbox if no notification ID was provided
    if not notification_id:
        return redirect("shared:notifications")

    # Ensure users can only view their own notifications
    notification = get_object_or_404(
        Notification,
        pk=notification_id,
        user=request.user,
    )

    # Handle POST action to mark the notification as read
    if request.method == "POST":
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        messages.success(request, "Notification marked as read.")
        return redirect("shared:notification_details", pk=notification.pk)

    return render(
        request,
        "shared/notification_details.html",
        {"notification": notification},
    )


@account_required
def profile_view(request):
    """Render the read-only profile page for the authenticated user."""
    return render(
        request,
        "shared/profile.html",
        {"profile": ensure_profile(request.user)},
    )


@account_required
def edit_profile_view(request):
    """Allow the authenticated user to update their editable contact number."""
    if request.method == "POST":
        request.user.contact_number = (
            request.POST.get("contact_number", "").strip() or None
        )
        request.user.save(update_fields=["contact_number"])

        messages.success(request, "Your profile has been updated successfully.")
        return redirect("shared:profile")

    return render(
        request,
        "shared/edit_profile.html",
        {"profile": ensure_profile(request.user)},
    )


@account_required
def settings_view(request):
    """Render the notification preferences settings page."""
    return render(request, "shared/settings.html")


@account_required
def help_support_view(request):
    """Render the Help & Support page (POST disabled until delivery backend is wired)."""
    if request.method == "POST":
        return render(
            request,
            "shared/help_support.html",
            {"error": "Support requests require a table or external delivery service."},
            status=400,
        )
    return render(request, "shared/help_support.html")