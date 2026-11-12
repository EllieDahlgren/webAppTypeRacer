from rest_framework import serializers

from .models import Passage, Race, RaceResult


class PassageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passage
        fields = ("id", "text", "difficulty")


class RaceResultSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    avatar = serializers.CharField(source="user.profile.avatar", read_only=True)

    class Meta:
        model = RaceResult
        fields = ("id", "username", "avatar", "wpm", "accuracy", "finished_at")


class RaceSerializer(serializers.ModelSerializer):
    passage = PassageSerializer(read_only=True)
    passage_id = serializers.PrimaryKeyRelatedField(
        queryset=Passage.objects.all(),
        source="passage",
        write_only=True,
        required=False,
    )
    results = RaceResultSerializer(many=True, read_only=True)

    class Meta:
        model = Race
        fields = ("id", "status", "started_at", "created_at", "passage", "passage_id", "results")
        read_only_fields = ("status", "started_at", "created_at")

class LeaderboardEntrySerializer(serializers.Serializer):
    username = serializers.CharField()
    avatar = serializers.CharField()
    best_wpm = serializers.FloatField()
    races = serializers.IntegerField()