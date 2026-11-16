from abc import ABC, abstractmethod
from .models import Notification, NotificationPreference


class Observer(ABC):
    @abstractmethod
    def update(self, subject) -> None:
        pass


class Subject(ABC):
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)


class NotificationSubject(Subject):
    def __init__(self):
        super().__init__()
        self.recipient = None
        self.title: str = ""
        self.message: str = ""
        self.notification_type: str = "account"

    def trigger_event(
        self, recipient, title: str, message: str, notification_type: str = "account"
    ) -> None:
        self.recipient = recipient
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.notify()


class InAppNotificationObserver(Observer):
    def update(self, subject: NotificationSubject) -> None:
        if subject.recipient is not None:
            Notification.objects.create(
                user=subject.recipient,
                title=subject.title,
                message=subject.message,
                notification_type=subject.notification_type,
            )


class PreferenceAwareObserver(Observer):
    def update(self, subject: NotificationSubject) -> None:
        if subject.recipient is None:
            return
        prefs, _ = NotificationPreference.objects.get_or_create(user=subject.recipient)
        if subject.notification_type == "timecard" and not prefs.timecard_updates:
            return
        if subject.notification_type == "leave" and not prefs.leave_updates:
            return