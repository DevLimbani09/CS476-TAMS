from django.conf import settings
from django.db import models


class Notification(models.Model):
    """Maps to the external Supabase 'notifications' table for cross-app user alerts."""

    TYPE_CHOICES = [
        ("timecard", "Timecards"),
        ("leave", "Leave"),
        ("time_tracking", "Time Tracking"),
        ("account", "Account"),
    ]

    notification_id = models.BigAutoField(primary_key=True)
    # Links each notification to the recipient's custom employee_id in the auth user model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        to_field="employee_id",
        db_column="recipient_id",
        related_name="notifications",
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(max_length=255, db_column="short_description")
    message = models.CharField(max_length=255, db_column="description")
    notification_type = models.CharField(max_length=255, db_column="type")
    is_read = models.BooleanField(db_column="read_status")
    created_at = models.DateTimeField(db_column="creation_date")

    class Meta:
        # Table schema is managed externally in Supabase rather than Django migrations
        managed = False
        db_table = "notifications"
        ordering = ["-created_at"]