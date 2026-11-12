from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Passage, Race, RaceResult
from .serializers import PassageSerializer, RaceSerializer


class PassageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Passage.objects.all()
    serializer_class = PassageSerializer


class RaceViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RaceSerializer

    def get_queryset(self):
        # select_related / prefetch_related avoid the "N+1 queries" problem
        return (
            Race.objects.select_related("passage")
            .prefetch_related("results__user__profile")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        passage = serializer.validated_data.get("passage") or Passage.objects.order_by("?").first()
        if passage is None:
            raise ValidationError({"detail": "No passages exist yet. Run seed_passages."})
        with transaction.atomic():
            race = serializer.save(passage=passage)
            RaceResult.objects.create(race=race, user=self.request.user)

    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):
        race = self.get_object()
        if race.status != Race.Status.WAITING:
            return Response({"detail": "This race has already started."}, status=400)
        RaceResult.objects.get_or_create(race=race, user=request.user)
        # re-fetch so the response includes the newly added player
        race = self.get_queryset().get(pk=race.pk)
        return Response(self.get_serializer(race).data)