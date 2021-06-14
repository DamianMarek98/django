import sys

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView

from django.db import models
from django.views.generic.edit import ModelFormMixin
from .forms import RegisterForm, CommentForm, TeamForm, PlayerForm, MatchForm

from .models import Team, Player, Match, Comment


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'league/login.html')


def team(request):
    team_id = request.GET.get('team_id', '')
    team_obj = get_object_or_404(Team, pk=team_id)
    players = Player.objects.filter(team_id=team_obj.id)

    team_form = None
    if request.method == "POST":
        team_form = TeamForm(request.POST)
        if team_form.is_valid():
            team_form.save()
            return redirect("/table")

    if team_form == None:
        team_form = TeamForm()

    return render(request, 'league/team.html', {'team': team_obj, 'players': players, 'team_form': team_form})


def profile(request):
    profile_id = request.GET.get('profile_id', '')
    player_obj = get_object_or_404(Player, pk=profile_id)
    return render(request, 'league/profile.html', {'player' : player_obj})


def match(request):
    match_id = request.GET.get('match_id', '')
    match_obj = get_object_or_404(Match, pk=match_id)
    comments = Comment.objects.filter(match_id=match_obj.id)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.match = match_obj
            new_comment.user = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'league/match_details.html', {'match' : match_obj, 'comments': comments,
                                                         'new_comment': new_comment,
                                                         'comment_form': comment_form})


def register(response):
    form = None
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")

    if form == None:
        form = RegisterForm()
    return render(response, 'league/register.html', {'form': form})


class Table(ListView, ModelFormMixin):
    model = Team
    ordering = ['-points']
    form_class = TeamForm
    form_class2 = PlayerForm
    form_class3 = MatchForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.team_form = self.get_form(self.form_class)
        self.player_form = self.get_form(self.form_class2)
        self.match_form = self.get_form(self.form_class3)
        # Explicitly states what get to call:
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # When the form is submitted, it will enter here
        self.object = None
        self.team_form = self.get_form(self.form_class)
        self.player_form = self.get_form(self.form_class2)
        self.match_form = self.get_form(self.form_class3)

        if self.team_form.is_valid():
            self.object = self.team_form.save()
            self.team_form = self.get_form(self.form_class)
            self.player_form = self.get_form(self.form_class2)
            self.match_form = self.get_form(self.form_class3)
        elif self.player_form.is_valid():
            self.object = self.player_form.save()
            self.team_form = self.get_form(self.form_class)
            self.player_form = self.get_form(self.form_class2)
            self.match_form = self.get_form(self.form_class3)
        elif self.match_form.is_valid():
            self.object = self.match_form.save()
            self.team_form = self.get_form(self.form_class)
            self.player_form = self.get_form(self.form_class2)
            self.match_form = self.get_form(self.form_class3)

        # Whether the form validates or not, the view will be rendered by get()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        # Just include the form
        context = super(Table, self).get_context_data(*args, **kwargs)
        context['team_form'] = self.team_form
        context['player_form'] = self.player_form
        context['match_form'] = self.match_form
        return context


class Matches(ListView):
    model = Match


