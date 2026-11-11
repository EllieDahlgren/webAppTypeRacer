from django.contrib import admin
from .models import Passage, Race, RaceResult


class RaceResultInline(admin.TabularInline):
    model = RaceResult
    extra = 0


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    inlines = [RaceResultInline]
    list_display = ("id", "status", "passage", "player_count")

    def player_count(self, obj):
        return obj.players.count()


admin.site.register(Passage)
admin.site.register(RaceResult)