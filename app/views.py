from django.shortcuts  import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from app.models import *
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

def home(request):
	return render_to_response('home.html',RequestContext(request))

@login_required
def index(request):
	return render_to_response('index.html',RequestContext(request))

@login_required
def pages(request, pk):
    event = Events.objects.get(pk=int(pk))
    last = Events.objects.order_by('-envio')[:5]
    d = dict(event=event, last=last)
    return render_to_response("pages.html", d, RequestContext(request))
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/principal/')
    else:
        return HttpResponseRedirect('/pages/')