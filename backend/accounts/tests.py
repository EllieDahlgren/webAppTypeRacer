from django.contrib.auth.models import User
from rest_framework.test import APITestCase

GOOD_PASSWORD = "Str0ngPass!234"


class AuthTests(APITestCase):
    def register(self, username="alice", password=GOOD_PASSWORD):
        return self.client.post(
            "/api/auth/register/",
            {"username": username, "email": f"{username}@example.com", "password": password},
            format="json",
        )

    def test_register_creates_user_and_profile(self):
        response = self.register()
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="alice")
        self.assertTrue(hasattr(user, "profile"))

    def test_register_rejects_weak_password(self):
        response = self.register(password="123")
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

    def test_login_returns_tokens(self):
        self.register()
        response = self.client.post(
            "/api/auth/login/",
            {"username": "alice", "password": GOOD_PASSWORD},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_requires_login(self):
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, 401)

    def test_me_returns_profile_when_logged_in(self):
        user = User.objects.create_user("bob", "bob@example.com", GOOD_PASSWORD)
        self.client.force_authenticate(user=user)
        response = self.client.get("/api/me/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["username"], "bob")
        self.assertEqual(response.data["avatar"], "car-1")