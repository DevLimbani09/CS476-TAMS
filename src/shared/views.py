from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from .models import Notification, NotificationPreference, SupportRequest, UserProfile
from .observers import InAppNotificationObserver, NotificationSubject

User = get_user_model()


def dashboard_view(request):
    unread_count = 0
    recent_notifications = []
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        recent_notifications = Notification.objects.filter(user=request.user)[:5]
    context = {
        "weekly_hours": "0.0 hrs",
        "timecard_status": "Not Started",
        "pending_requests": 0,
        "unread_count": unread_count,
        "recent_notifications": recent_notifications,
    }
    return render(request, "shared/dashboard.html", context)


def notifications_view(request):
    notifications = Notification.objects.none()
    unread_count = 0
    read_status = request.GET.get("read_status", "all")
    notification_type = request.GET.get("notification_type", "all")

    if request.user.is_authenticated:
        qs = Notification.objects.filter(user=request.user)
        unread_count = qs.filter(is_read=False).count()
        if read_status == "unread":
            qs = qs.filter(is_read=False)
        elif read_status == "read":
            qs = qs.filter(is_read=True)
        if notification_type != "all":
            qs = qs.filter(notification_type=notification_type)
        notifications = qs

    context = {
        "notifications": notifications,
        "unread_count": unread_count,
        "selected_status": read_status,
        "selected_type": notification_type,
    }
    return render(request, "shared/notifications.html", context)


def notification_details_view(request, pk=None):
    notification = None
    if request.user.is_authenticated and pk is not None:
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        if request.method == "POST":
            notification.is_read = True
            notification.save()
            return redirect("shared:notification_details", pk=notification.pk)
    return render(
        request, "shared/notification_details.html", {"notification": notification}
    )


def profile_view(request):
    profile = None
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "employee_id": f"EMP-{request.user.id:04d}",
                "preferred_name": request.user.get_full_name() or request.user.username,
            },
        )
    return render(request, "shared/profile.html", {"profile": profile})


def edit_profile_view(request):
    profile = None
    success = False
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={
                "employee_id": f"EMP-{request.user.id:04d}",
                "preferred_name": request.user.get_full_name() or request.user.username,
            },
        )
        if request.method == "POST":
            profile.preferred_name = request.POST.get("preferred_name", "").strip()
            profile.contact_number = request.POST.get("contact_number", "").strip()
            if "profile_picture" in request.FILES:
                profile.profile_picture = request.FILES["profile_picture"]
            profile.save()
            success = True
    return render(
        request,
        "shared/edit_profile.html",
        {"profile": profile, "success": success},
    )


def settings_view(request):
    prefs = None
    success = False
    if request.user.is_authenticated:
        prefs, _ = NotificationPreference.objects.get_or_create(user=request.user)
        if request.method == "POST":
            prefs.timecard_updates = request.POST.get("timecard_updates") == "yes"
            prefs.leave_updates = request.POST.get("leave_updates") == "yes"
            prefs.deadline_reminders = request.POST.get("deadline_reminders") == "yes"
            prefs.save()
            success = True
    return render(
        request, "shared/settings.html", {"prefs": prefs, "success": success}
    )


def help_support_view(request):
    success = False
    if request.method == "POST":
        category = request.POST.get("support_category", "other")
        subject_text = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()
        if subject_text and message_text:
            SupportRequest.objects.create(
                user=request.user if request.user.is_authenticated else None,
                support_category=category,
                subject=subject_text,
                message=message_text,
            )
            subject_notifier = NotificationSubject()
            subject_notifier.attach(InAppNotificationObserver())
            for admin_user in User.objects.filter(is_staff=True):
                subject_notifier.trigger_event(
                    recipient=admin_user,
                    title=f"Support Request: {subject_text}",
                    message=message_text,
                    notification_type="account",
                )
            success = True
    return render(request, "shared/help_support.html", {"success": success})