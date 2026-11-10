from django.db import models

class Passage(models.Model):
    text = models.TextField()
    difficulty = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.text[:50]
