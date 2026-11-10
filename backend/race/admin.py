from django.contrib import admin
from .models import Passage, Race, RaceResult

admin.site.register(Passage)
admin.site.register(Race)
admin.site.register(RaceResult)