from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.CharField(max_length=32, default="car-1")
    best_wpm = models.FloatField(default=0)

    def __str__(self):
        return f"Profile for {self.user.username}"