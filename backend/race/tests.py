from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework.test import APITestCase

from .models import Passage, Race, RaceResult


class RaceApiTests(APITestCase):
    def setUp(self):
        self.passage = Passage.objects.create(text="The quick brown fox.", difficulty=1)
        self.alice = User.objects.create_user("alice", "alice@example.com", "Str0ngPass!234")
        self.bob = User.objects.create_user("bob", "bob@example.com", "Str0ngPass!234")

    def test_races_require_login(self):
        response = self.client.get("/api/races/")
        self.assertEqual(response.status_code, 401)

    def test_create_race_adds_creator_as_player(self):
        self.client.force_authenticate(user=self.alice)
        response = self.client.post("/api/races/", {}, format="json")
        self.assertEqual(response.status_code, 201)
        race = Race.objects.get(pk=response.data["id"])
        self.assertEqual(race.status, Race.Status.WAITING)
        self.assertEqual(list(race.players.all()), [self.alice])

    def test_join_waiting_race(self):
        race = Race.objects.create(passage=self.passage)
        self.client.force_authenticate(user=self.bob)
        response = self.client.post(f"/api/races/{race.id}/join/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(race.results.count(), 1)

    def test_join_twice_does_not_duplicate(self):
        race = Race.objects.create(passage=self.passage)
        self.client.force_authenticate(user=self.bob)
        self.client.post(f"/api/races/{race.id}/join/")
        self.client.post(f"/api/races/{race.id}/join/")
        self.assertEqual(race.results.count(), 1)

    def test_cannot_join_running_race(self):
        race = Race.objects.create(passage=self.passage, status=Race.Status.RUNNING)
        self.client.force_authenticate(user=self.bob)
        response = self.client.post(f"/api/races/{race.id}/join/")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(race.results.count(), 0)


class ConstraintTests(APITestCase):
    def setUp(self):
        self.passage = Passage.objects.create(text="Hello there.")
        self.user = User.objects.create_user("carol", "carol@example.com", "Str0ngPass!234")
        self.race = Race.objects.create(passage=self.passage)

    def test_negative_wpm_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                RaceResult.objects.create(race=self.race, user=self.user, wpm=-5, accuracy=90)

    def test_accuracy_over_100_is_rejected(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                RaceResult.objects.create(race=self.race, user=self.user, wpm=50, accuracy=150)

    def test_same_user_cannot_join_race_twice(self):
        RaceResult.objects.create(race=self.race, user=self.user)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                RaceResult.objects.create(race=self.race, user=self.user)


class LeaderboardTests(APITestCase):
    def test_leaderboard_sorted_by_best_wpm(self):
        passage = Passage.objects.create(text="Test passage.")
        slow = User.objects.create_user("slow", "slow@example.com", "Str0ngPass!234")
        fast = User.objects.create_user("fast", "fast@example.com", "Str0ngPass!234")
        race1 = Race.objects.create(passage=passage)
        race2 = Race.objects.create(passage=passage)
        RaceResult.objects.create(race=race1, user=slow, wpm=40, accuracy=95)
        RaceResult.objects.create(race=race1, user=fast, wpm=80, accuracy=98)
        RaceResult.objects.create(race=race2, user=fast, wpm=70, accuracy=96)

        self.client.force_authenticate(user=slow)
        response = self.client.get("/api/leaderboard/")
        self.assertEqual(response.status_code, 200)
        rows = response.data["results"]
        self.assertEqual([r["username"] for r in rows], ["fast", "slow"])
        self.assertEqual(rows[0]["best_wpm"], 80)
        self.assertEqual(rows[0]["races"], 2)