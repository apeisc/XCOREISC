from django.shortcuts  import render_to_response,redirect
from django.http import HttpResponseRedirect,HttpResponse
from app.models import *
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms
from django.conf import settings
from PIL import Image as PImage
from os.path import join as pjoin

class EventForm(ModelForm):
    class Meta:
        model = Events
class UserForm(ModelForm):
    class Meta:
        model = User
class UserProfileForm(forms.ModelForm):
    tipo = forms.TypedChoiceField(choices = TIPOS)
    class Meta:
        model = UserProfile
        exclude = [ "user"]
        avatar = forms.ImageField()

def index(request):
    post = Post.objects.all().order_by('-pk')
    publi = Patrocina.objects.all().order_by('-pk')
    form = UserProfileForm()
    form2 = UserForm()
    d =  dict(post=post,publi=publi,form=form,form2=form2)
    if request.user.is_authenticated():
        return render_to_response("index.html", d, RequestContext(request))
    else:
        return render_to_response("registration/login.html", d, RequestContext(request))


def process(request):
    if request.method=="POST": 
        print request.POST  
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/process/complete/')   
    else:
        form = UserProfileForm()
    d=dict(form=form)
    return render_to_response("registration/login.html", d, RequestContext(request)) 


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
    publi = Patrocina.objects.get(pk=int(pk))
    try:
        asis = Patrocina.objects.get(recomienda=request.user,pk=pk)
    except Patrocina.DoesNotExist:
        asis = None
    d = dict(publi=publi,asis=asis)
    return render_to_response("auspicio.html", d, RequestContext(request))

def checkUser(request):
    if request.is_ajax(): 
        try:
            very = User.objects.get(username=request.GET.get('b',''))
        except User.DoesNotExist:
            very = None
        if very:
            msg = False
        else:
            msg = True
    else:
        msg = False
    return HttpResponse(msg)

def checkTrans(request):
    if request.is_ajax(): 
        try:
            very = UserProfile.objects.get(n_trans=request.GET.get('b',''))
        except UserProfile.DoesNotExist:
            very = None
        if very:
            msg = False
        else:
            msg = True
    else:
        msg = False
    return HttpResponse(msg)

def checkEmail(request):
    if request.is_ajax(): 
        try:
            very = User.objects.get(email=request.GET.get('b',''))
        except User.DoesNotExist:
            very = None
        if very:
            msg = False
        else:
            msg = True
    else:
        msg = False
    return HttpResponse(msg)


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
        asis = Patrocina.objects.get(recomienda=request.user,pk=int(pk))
    except Patrocina.DoesNotExist:
        asis = None
    if not asis:
        new = Patrocina.objects.get(pk=int(pk))
        new.recomienda.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required   
def removePubli(request,pk):
    try:
        asis = Patrocina.objects.get(recomienda=request.user,pk=int(pk))
    except Patrocina.DoesNotExist:
        asis = None
    if asis:
        asis.recomienda.remove(request.user)       
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))       

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def edit_user(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method=="POST":   
        print request.POST
        asis = UserProfileForm(request.POST,request.FILES,instance=profile)
        if asis.is_valid():
            asis.save()
            imfn = pjoin(settings.MEDIA_ROOT, profile.avatar.name)
            im = PImage.open(imfn)
            im.thumbnail((160,160), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

def auth_view(request):
    if request.method=='POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/')
        else:
            msg = 'Verifique los datos, posiblemente aun no se encuentre activada su cuenta asi que le regamos que revise su Email para confirmar, o vuelva a intentarlo en breves minutos'
            return render_to_response('registration/login.html', {'msg': msg }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')    