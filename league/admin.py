from django.contrib import admin

from .models import Match, Team, Player, Comment


class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'home_score', 'away_score')
admin.site.register(Match, MatchAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'points')
admin.site.register(Team, TeamAdmin)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'user', 'team', 'number')
admin.site.register(Player, PlayerAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'date_created', 'user', 'match')
admin.site.register(Comment, CommentAdmin)