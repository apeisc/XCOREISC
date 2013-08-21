from django.forms import ModelForm
from django import forms
from app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

class PonenteForm(ModelForm):
    class Meta:
        model = Ponente

class EventForm(ModelForm):
    class Meta:
        model = Events

