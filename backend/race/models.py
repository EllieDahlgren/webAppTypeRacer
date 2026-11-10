from django.contrib.auth.models import User
from django.db import models

class Passage(models.Model):
    text = models.TextField()
    difficulty = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.text[:50]

class Race(models.Model):
    class Status(models.TextChoices):
        WAITING = "waiting", "Waiting"
        RUNNING = "running", "Running"
        FINISHED = "finished", "Finished"

    passage = models.ForeignKey(Passage, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.WAITING)
    started_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Race {self.id} ({self.status})"

class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="results")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    wpm = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["race", "user"], name="one_result_per_user_race"),
        ]

    def __str__(self):
        return f"{self.user.username} in race {self.race_id}"