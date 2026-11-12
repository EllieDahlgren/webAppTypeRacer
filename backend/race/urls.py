from rest_framework.routers import DefaultRouter

from .views import PassageViewSet, RaceViewSet

router = DefaultRouter()
router.register("passages", PassageViewSet, basename="passage")
router.register("races", RaceViewSet, basename="race")

urlpatterns = router.urls