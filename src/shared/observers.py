"""Gang of Four (GoF) Observer pattern implementation for TAMS in-app notifications."""

from abc import ABC, abstractmethod

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Notification


class Observer(ABC):
    """Abstract observer interface subscribed to notification events."""

    @abstractmethod
    def update(self, subject):
        """Handle a state update published by the attached subject."""
        pass


class Subject:
    """Base observable subject that maintains and notifies attached observers."""

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Register an observer if it is not already subscribed."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Unsubscribe an observer from future notifications."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """Broadcast the latest event state to all attached observers."""
        for observer in tuple(self._observers):
            observer.update(self)


class NotificationSubject(Subject):
    """Concrete subject that validates notification payloads before notifying observers."""

    def trigger_event(
        self,
        recipient,
        title,
        message,
        notification_type="account",
    ):
        # Validate required fields before broadcasting to observers
        if recipient is None:
            raise ValidationError("Notification recipient is required.")

        valid_types = dict(Notification.TYPE_CHOICES)
        if notification_type not in valid_types:
            raise ValidationError("Invalid notification type.")

        if not str(title).strip():
            raise ValidationError("Notification title is required.")

        if not str(message).strip():
            raise ValidationError("Notification message is required.")

        self.recipient = recipient
        self.title = str(title)
        self.message = str(message)
        self.notification_type = notification_type

        self.notify()


class InAppNotificationObserver(Observer):
    """Concrete observer that writes a new unread Notification row to the database."""

    def update(self, subject):
        Notification.objects.create(
            user=subject.recipient,
            title=subject.title[:255],
            message=subject.message[:255],
            notification_type=subject.notification_type,
            is_read=False,
            created_at=timezone.now(),
        )


class PreferenceAwareObserver(InAppNotificationObserver):
    """Extension hook for filtering alerts by user notification preferences."""

    pass