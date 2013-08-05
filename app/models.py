from django.db import models
from django.contrib.auth.models import User


'''class UserProfile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to="media/", blank=True, null=True)
    user = models.ForeignKey(User,unique=True)
    def __unicode__(self):
        return unicode(self.user)'''
class Ponente(models.Model):
	nombre = models.CharField(max_length=50)
	avatar = models.ImageField(upload_to='ponentes/', verbose_name='Imagen')
	body = models.TextField(verbose_name='Caracteristicas')
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
    Asistencia = models.IntegerField(default=0)
    banner = models.ImageField("Banner 850x350", upload_to="banners/", blank=True, null=True)
    def __unicode__(self):
        return self.title

