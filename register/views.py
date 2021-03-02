from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from . import models
from transcribe_audio.models import AudioDataModel
# Create your views here.

def signin_home_page(request):
    return render(request,"signin_home.html")

def signin_form_page(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        
    return render(request,"signin_form.html")

def register_form_page(request):
    return render(request,"register_form.html")

def dashboard_page(request):
    return render(request,"dashboard.html")

def register_home_page(request):
    return render(request,"register_home.html")