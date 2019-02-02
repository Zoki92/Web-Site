from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
# Create your views here.


class HomeView(ListView):
    model = User
    template_name = 'base.html'