from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper

from .models import Comment, Team, Player, Match


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            "text": ("Tekst")
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'points',)
        labels = {
            "name": "Nazwa",
            "points": "Punkty",
        }


class MatchForm(forms.ModelForm):
    home_team = forms.ModelChoiceField(queryset=Team.objects.all(),
                                  to_field_name='name',
                                  empty_label="Wybierz gospodarza")
    away_team = forms.ModelChoiceField(queryset=Team.objects.all(),
                                       to_field_name='name',
                                       empty_label="Wybierz gościa")

    class Meta:
        model = Match
        fields = ('home_team', 'away_team', 'home_score', 'away_score')
        labels = {
            "home_team": "Gospodarz",
            "away_team": "Gość",
            "home_score": "Bramki gospodarza",
            "away_score": "Bramki gościa",
        }


class PlayerForm(forms.ModelForm):
    team = forms.ModelChoiceField(queryset=Team.objects.all(),
                                  to_field_name='name',
                                  empty_label="Wybierz zespół")

    class Meta:
        model = Player
        fields = ('name', 'surname', 'team', 'number')
        labels = {
            "team": "Zespół",
            "number": "Numer",
            "name": "Imie",
            "surname": "Nazwisko",
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
