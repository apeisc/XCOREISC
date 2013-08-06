from django.shortcuts  import render_to_response,redirect
from django.http import HttpResponseRedirect,HttpResponse
from app.models import *
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def home(request):
	return render_to_response('home.html',RequestContext(request))

@login_required
def index(request):
    post = Post.objects.all().order_by('-pk')
    publi = Publicidad.objects.all().order_by('-pk')
    d =  dict(post=post,publi=publi)
    return render_to_response("index.html", d, RequestContext(request))

@login_required
def pages(request, pk):
    event = Events.objects.get(pk=int(pk))
    try:
        asis = Events.objects.get(asistente=request.user,pk=pk)
    except Events.DoesNotExist:
        asis = None
    d = dict(event=event,asis=asis)
    return render_to_response("pages.html", d, RequestContext(request))

def auspicio(request, pk):
    publi = Publicidad.objects.get(pk=int(pk))
    try:
        asis = Publicidad.objects.get(recomienda=request.user,pk=pk)
    except Publicidad.DoesNotExist:
        asis = None
    d = dict(publi=publi,asis=asis)
    return render_to_response("auspicio.html", d, RequestContext(request))

def allpages(request):
    event = Events.objects.all()
    d =  dict(event=event)
    return render_to_response("allpages.html", d, RequestContext(request))

def post(user,event):
    try:
        view = Post.objects.get(asistente=user,event=event)
    except Post.DoesNotExist:
        view = None
    if not view:
        post = Post.objects.create(asistente=user,event=event)
        post.save()

def removePost(request, pk):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        Post.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def addEvent(request,pk):
    try:
        asis = Events.objects.get(asistente=request.user,pk=int(pk))
    except Events.DoesNotExist:
        asis = None
    if not asis:
        new = Events.objects.get(pk=int(pk))
        new.asistente.add(request.user)
        username = User.objects.get(username=request.user)
        post(username,new)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required   
def removeEvent(request,pk):
    try:
        asis = Events.objects.get(asistente=request.user,pk=int(pk))
    except Events.DoesNotExist:
        asis = None
    if asis:
        asis.asistente.remove(request.user)
    try:
        post = Post.objects.get(asistente=request.user,event=asis).delete()
    except Post.DoesNotExist:
        post = None    
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
 
@login_required
def addPubli(request,pk):
    try:
        asis = Publicidad.objects.get(recomienda=request.user,pk=int(pk))
    except Publicidad.DoesNotExist:
        asis = None
    if not asis:
        new = Publicidad.objects.get(pk=int(pk))
        new.recomienda.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required   
def removePubli(request,pk):
    try:
        asis = Publicidad.objects.get(recomienda=request.user,pk=int(pk))
    except Publicidad.DoesNotExist:
        asis = None
    if asis:
        asis.recomienda.remove(request.user)       
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))       

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