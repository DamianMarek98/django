from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .forms import RegisterForm

from .models import Team


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'league/login.html')


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


class Table(ListView):
    model = Team
