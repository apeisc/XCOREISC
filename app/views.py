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
from datetime import datetime 

class AlertForm(ModelForm):
    class Meta:
        model = Alertas
class EventForm(ModelForm):
    class Meta:
        model = Events
class UserForm(ModelForm):
    class Meta:
        model = User
'''class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ["event","asistente"]'''


class ThumbEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = [ "user","tipo","n_trans","active","fecha_trans","user2","dni","first_name","last_name","telefono","sexo"]
        avatar = forms.ImageField()

class UserProfileForm(forms.ModelForm):
    tipo = forms.TypedChoiceField(choices = TIPOS)
    sexo = forms.ChoiceField(choices= SEXO,widget=forms.RadioSelect)
    class Meta:
        model = UserProfile
        exclude = [ "user"]
        avatar = forms.ImageField()

def index(request):
    if request.user.is_authenticated():
        follow_post = Follow.objects.all().filter(user1=request.user)
        post        = Post.objects.all().order_by('-pk')
        publi       = Patrocina.objects.all().order_by('-pk')
        hotel       = Patrocina.objects.all().filter(tipo = 1)
        restaurant  = Patrocina.objects.all().filter(tipo = 2)
        movil       = Patrocina.objects.all().filter(tipo = 3)
        lugar       = Patrocina.objects.all().filter(tipo = 4)
        alert       = Alertas.objects.all().filter(usuario=request.user)
        user_all    = User.objects.all()
        
        d =  dict(post=post,
            publi=publi,
            follow_post=follow_post,
            hotel=hotel,
            movil = movil,
            restaurant=restaurant,
            lugar=lugar,
            user_all=user_all,
            alert=alert,
           
            )
        return render_to_response("index.html", d, RequestContext(request))
    else:
        form = UserProfileForm()
        form2 = UserForm()
        d =  dict(form=form,form2=form2)
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
        data = request.GET.get('b','')
        if data is not 'admin':
            try:
                very = User.objects.get(username=data)
            except User.DoesNotExist:
                very = None
            if very:
                msg = False
            else:
                msg = True
        else:
            msg=False
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

def new_user(request):
    UserF = UserCreationForm(request.POST or None)
    if request.method == "POST" and request.is_ajax():   
          
        '''print request.POST
        if UserF.is_valid():
            UserF.save()
            new = request.POST.copy()
            #if UserF.is_valid():
            u = User.objects.create_user(new['username'],
                                 new['email'],
                                 new['password1'])
            u.is_active = False
            u.save()
            msg="<div class='alert-box a-green'>Tu Quimera fue publicada con exito.<a href='#' class='submitBlue submitBlue-active'>Publicar</a></div>"
        else:
            msg="<div class='alert-box a-red'>Ocurrio un problema al enviar datos, verifica que esten completos.<a href='#' class='submitBlue submitBlue-active'>Publicar</a></div>"
    '''
        msg="<div class='alert-box a-green'>Tu Quimera fue publicada con exito.<a href='#' class='submitBlue submitBlue-active'>Publicar</a></div>"
        UserF.save()   
    else:
        msg = "GET petitions are not allowed for this view."
    return HttpResponse(msg)

def allpages(request):
    event = Events.objects.all()
    d =  dict(event=event)
    
    return render_to_response("allpages.html", d, RequestContext(request))
    
'''def posting(request):
    if request.method == "POST":
        post = PostForm(request.POST)
        if post.is_valid():
            usuario = User.objects.get(username=request.user)
            date = post.save(commit=False)
            date.asistente = usuario
            date.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))'''

def post(user,event,texto):
    try:
        view = Post.objects.get(asistente=user,event=event)
    except Post.DoesNotExist:
        view = None
    if not view:
        post = Post.objects.create(asistente=user,event=event,body=texto)
        post.save()

def removePost(request, pk):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        Post.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def addEvent(request,pk):
    if request.method == 'POST':
        try:
            asis = Events.objects.get(asistente=request.user,pk=int(pk))
        except Events.DoesNotExist:
            asis = None
        if not asis:
            new = Events.objects.get(pk=int(pk))
            new.asistente.add(request.user)
            username = User.objects.get(username=request.user)
            body = request.POST.get('body','')
            post(username,new,body)
    return HttpResponseRedirect('/evento/'+pk)

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
    return HttpResponseRedirect('/evento/'+pk)
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
        asis = ThumbEditForm(request.POST,request.FILES,instance=profile)
        if asis.is_valid():
            asis.save()
            imfn = pjoin(settings.MEDIA_ROOT, profile.avatar.name)
            im = PImage.open(imfn)
            im.thumbnail((240,240), PImage.ANTIALIAS)
            im.save(imfn, "JPEG")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

#planifica seccion
def planifica(request):
    event = Events.objects.all().order_by('fecha').filter(asistente = request.user)
    d =  dict(event=event)
    return render_to_response("planifica.html", d, RequestContext(request))

#seccion user profile
def account(request, username):
    try:
        username = User.objects.get(username=username)
    except User.DoesNotExist:
        username = None
    post = Post.objects.all().order_by('-pk').filter(asistente=username)
    follow = Follow.objects.filter(user1=request.user,user2=username)
    count_follow = Follow.objects.all().filter(user1=username)
    count_follower = Follow.objects.all().filter(user2=username)
    Alert = AlertForm()
    d =  dict(username=username,post=post,follow=follow,count_follow=count_follow,count_follower=count_follower,Alert=Alert)
    if username is not None:
        return render_to_response("profile.html", d, RequestContext(request))
    else:
        return HttpResponseRedirect('/')#cambiar esto
    
def follow(request,username):
    try:
        username = User.objects.get(username=username)
    except User.DoesNotExist:
        username = None
    if username is not request.user:
        if username is not None:
            try:
                follow = Follow.objects.get(user1=request.user,user2=username)
            except Follow.DoesNotExist:
                follow = None
            if follow is None:
                follower = Follow.objects.create(user1=request.user,user2=username)
                follower.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

def nofollow(request,username):
    try:
        username = User.objects.get(username=username)
    except User.DoesNotExist:
        username = None
    if username is not request.user:
        if username is not None:
            try:
                follow = Follow.objects.get(user1=request.user,user2=username)
            except Follow.DoesNotExist:
                follow = None
            if follow is not None:
                Follow.objects.filter(user1=request.user,user2=username).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

def alert(request,pk):
    try:
        alert = Alertas.objects.filter(pk=int(pk),usuario=request.user)
    except Alertas.DoesNotExist:
        alert = None
    if alert is not None:
        alert.update(visto=True)
    return HttpResponseRedirect('/')      
  
def Notificar(request,username):
  
  if request.method == "POST":
    if request.user.is_staff:
      Username = User.objects.get(username=username)
      mensaje = request.POST.get('mensaje','')
      tipo = request.POST.get('tipo','')
      Alertas.objects.create(tipo=tipo,usuario=Username,mensaje=mensaje,visto=False)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
def auth_view(request):
    if request.method=='POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        '''try:
            estado = UserProfile.objects.get(user2=username,active=True)
        except UserProfile.DoesNotExist:
            estado = None
        if estado is not None and user is not None:'''
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/')
        else:
            msg = 'Verifique los datos, posiblemente que aun  su cuenta no se encuentre activada asi que le regamos que revise su Email para confirmar, o vuelva a intentarlo en breves minutos'
            return render_to_response('registration/login.html', {'msg': msg }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')    