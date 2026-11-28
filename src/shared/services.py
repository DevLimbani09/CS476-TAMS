"""Service layer helpers for publishing cross-app notifications safely."""

from django.db import transaction

from .observers import (
    InAppNotificationObserver,
    NotificationSubject,
)


def send_notification(
    recipient,
    title,
    message,
    notification_type="account",
):
    """
    Schedule a TAMS in-app notification to fire only after the active
    database transaction commits successfully.
    """
    if recipient is None:
        return

    def publish():
        # Wire up the subject and in-app observer, then dispatch the event
        subject = NotificationSubject()
        observer = InAppNotificationObserver()
        subject.attach(observer)

        subject.trigger_event(
            recipient=recipient,
            title=title,
            message=message,
            notification_type=notification_type,
        )

    transaction.on_commit(publish)