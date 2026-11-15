from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    preferred_name = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=30, unique=True)
    contact_number = models.CharField(max_length=25, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    department = models.CharField(max_length=100, default="Engineering")
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="direct_reports",
    )
    account_status = models.CharField(max_length=30, default="Active")

    def __str__(self):
        return f"{self.preferred_name or self.user.username} ({self.employee_id})"


class Notification(models.Model):
    TYPE_CHOICES = [
        ("timecard", "Timecards"),
        ("leave", "Leave"),
        ("time_tracking", "Time Tracking"),
        ("account", "Account"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default="account"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} -> {self.user.username}"


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_preference",
    )
    timecard_updates = models.BooleanField(default=True)
    leave_updates = models.BooleanField(default=True)
    deadline_reminders = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"


class SupportRequest(models.Model):
    CATEGORY_CHOICES = [
        ("account", "Account or Login"),
        ("timecard", "Timecards"),
        ("time_tracking", "Time Tracking"),
        ("leave", "Leave"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="support_requests",
    )
    support_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subject = models.CharField(max_length=150)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.support_category}] {self.subject}"