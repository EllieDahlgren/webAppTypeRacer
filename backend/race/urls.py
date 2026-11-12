from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LeaderboardView, PassageViewSet, RaceViewSet

router = DefaultRouter()
router.register("passages", PassageViewSet, basename="passage")
router.register("races", RaceViewSet, basename="race")

urlpatterns = [
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
] + router.urls