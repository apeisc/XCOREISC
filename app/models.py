from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to="thum/", blank=True, null=True)
    user = models.ForeignKey(User,unique=True)
    def __unicode__(self):
        return unicode(self.user)
class Pais(models.Model):
    nombre = models.CharField(max_length=50)
    bandera = models.ImageField(upload_to='bandera/', verbose_name='bandera')
    def __unicode__(self):
        return self.nombre

class Ponente(models.Model):
    nombre = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='ponentes/', verbose_name='Imagen')
    body = models.TextField(verbose_name='Caracteristicas')
    Pais = models.ForeignKey(Pais)
    def __unicode__(self):
    	return self.nombre
    def ponente_thumb(self):
        return u'<img src="/media/%s" width="50" height="50" />' % (self.avatar)
    ponente_thumb.allow_tags = True


class Events(models.Model):
    title = models.CharField(max_length=200,verbose_name='Titulo')
    body = models.TextField(verbose_name='Caracteristicas')
    fecha = models.DateTimeField()
    ponente = models.ForeignKey(Ponente)
    asistente = models.ManyToManyField(User ,help_text='ASISTENTES',blank=True)
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
    """When creating a new user, make a profile for him."""
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)