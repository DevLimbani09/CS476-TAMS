from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Notification, NotificationPreference, SupportRequest, UserProfile


class SharedModuleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123",
        )
        self.client.force_login(self.user)

    def test_all_seven_pages_render_200(self):
        urls = [
            reverse("shared:dashboard"),
            reverse("shared:notifications"),
            reverse("shared:notification_details_default"),
            reverse("shared:profile"),
            reverse("shared:edit_profile"),
            reverse("shared:settings"),
            reverse("shared:help_support"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Failed on {url}")

    def test_edit_profile_updates_database(self):
        response = self.client.post(
            reverse("shared:edit_profile"),
            {
                "preferred_name": "Meet Patel",
                "contact_number": "306-555-0199",
            },
        )
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.preferred_name, "Meet Patel")
        self.assertEqual(profile.contact_number, "306-555-0199")

    def test_settings_preferences_save(self):
        response = self.client.post(
            reverse("shared:settings"),
            {
                "timecard_updates": "yes",
                "deadline_reminders": "yes",
            },
        )
        self.assertEqual(response.status_code, 200)
        prefs = NotificationPreference.objects.get(user=self.user)
        self.assertTrue(prefs.timecard_updates)
        self.assertFalse(prefs.leave_updates)
        self.assertTrue(prefs.deadline_reminders)

    def test_help_support_creates_request_and_notification(self):
        admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword123",
            is_staff=True,
        )
        response = self.client.post(
            reverse("shared:help_support"),
            {
                "support_category": "timecard",
                "subject": "Missing Monday hours",
                "message": "Need help logging Monday shift.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SupportRequest.objects.filter(user=self.user).count(), 1)
        # Verifies observer generated an in-app notification for staff/admin
        self.assertTrue(Notification.objects.filter(user=admin_user).exists())

    def test_notification_details_and_mark_as_read(self):
        notif = Notification.objects.create(
            user=self.user,
            title="Test Alert",
            notification_type="account",
            message="Hello world",
            is_read=False,
        )
        detail_url = reverse("shared:notification_details", args=[notif.pk])
        get_resp = self.client.get(detail_url)
        self.assertEqual(get_resp.status_code, 200)
        self.assertContains(get_resp, "Test Alert")

        post_resp = self.client.post(detail_url)
        self.assertEqual(post_resp.status_code, 302)
        notif.refresh_from_db()
        self.assertTrue(notif.is_read)