from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.forms import ModelForm
from django import forms


class UserProfile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to="thum/", blank=True, null=True)
    user = models.ForeignKey(User,unique=True)
    def __unicode__(self):
        return unicode(self.user)

class Paises(models.Model):
    nombre = models.CharField(max_length=50)
    bandera = models.ImageField(upload_to='bandera/', verbose_name='bandera')


class Ponente(models.Model):
    nombre = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='ponentes/', verbose_name='Imagen')
    body = models.TextField(verbose_name='Caracteristicas')
    pais = models.ForeignKey(Paises)
    def __unicode__(self):
            return self.title
    def ponente_thumb(self):
        return u'<img src="/media/%s" width="50" height="50" />' % (self.avatar)
    ponente_thumb.allow_tags = True

class Events(models.Model):
    title = models.CharField(max_length=200,verbose_name='Titulo')
    body = models.TextField(verbose_name='Caracteristicas')
    fecha = models.DateTimeField()
    ponente = models.ForeignKey(Ponente)
    asistente = models.ManyToManyField(User ,help_text='ASISTENTES',blank=True, null=True)
    banner = models.ImageField("Banner 850x350", upload_to="banners/", blank=True, null=True)
    def __unicode__(self):
        return self.title

class Publicidad(models.Model):
    nombre = models.CharField(max_length=200)
    body = models.TextField(verbose_name='Caracteristicas')
    direccion = models.CharField(max_length=200)
    recomienda = models.ManyToManyField(User,blank=True)
    banner = models.ImageField("Banner 850x350", upload_to="banners/", blank=True, null=True)
    bannerIndex = models.ImageField("Banner 250x250", upload_to="index/", blank=True)
    def __unicode__(self):
        return self.nombre


class Post(models.Model):
    asistente = models.ForeignKey(User)
    event = models.ForeignKey(Events)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.user    

def create_user_profile(sender, **kwargs):
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)

class PonenteForm(ModelForm):
    class Meta:
        model = Ponente

class EventForm(ModelForm):
    class Meta:
        model = Events

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['ponente'].widget.attrs.update({'class' : 'form-control'})

