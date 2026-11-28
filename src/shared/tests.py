from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Notification
from .observers import InAppNotificationObserver, NotificationSubject
from .services import send_notification

User = get_user_model()


class SharedBackendTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Temporarily allow Django to create the unmanaged 'notifications' table in the test DB
        Notification._meta.managed = True
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        Notification._meta.managed = False

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
            employee_id="EMP1001",
            contact_number="306-555-0100",
            account_status=True,
        )
        self.client.force_login(self.user)

    def test_observer_creates_unread_notification(self):
        subject = NotificationSubject()
        observer = InAppNotificationObserver()
        subject.attach(observer)

        subject.trigger_event(
            recipient=self.user,
            title="Timecard Approved",
            message="Your weekly timecard has been approved.",
            notification_type="timecard",
        )

        notif = Notification.objects.get(user=self.user)
        self.assertEqual(notif.title, "Timecard Approved")
        self.assertEqual(notif.notification_type, "timecard")
        self.assertFalse(notif.is_read)

    def test_subject_rejects_invalid_payload(self):
        subject = NotificationSubject()
        with self.assertRaises(ValidationError):
            subject.trigger_event(
                recipient=self.user,
                title="",
                message="Valid message",
                notification_type="invalid_type",
            )

    def test_send_notification_service_on_commit(self):
        with self.captureOnCommitCallbacks(execute=True):
            send_notification(
                recipient=self.user,
                title="Leave Update",
                message="Your leave request was reviewed.",
                notification_type="leave",
            )

        self.assertTrue(
            Notification.objects.filter(user=self.user, title="Leave Update").exists()
        )

    def test_notifications_list_and_mark_as_read(self):
        notif = Notification.objects.create(
            user=self.user,
            title="Account Notice",
            message="Welcome to TAMS.",
            notification_type="account",
            is_read=False,
            created_at="2026-11-28T00:00:00Z",
        )

        list_resp = self.client.get(reverse("shared:notifications"))
        self.assertEqual(list_resp.status_code, 200)
        self.assertContains(list_resp, "Account Notice")

        detail_url = reverse("shared:notification_details", args=[notif.pk])
        post_resp = self.client.post(detail_url)
        self.assertEqual(post_resp.status_code, 302)

        notif.refresh_from_db()
        self.assertTrue(notif.is_read)

    def test_edit_profile_updates_contact_number(self):
        response = self.client.post(
            reverse("shared:edit_profile"),
            {"contact_number": "306-555-9999"},
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.contact_number, "306-555-9999")