from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

TIPOS= (
    ('1', 'Estudiante'),
    ('2', 'Profesional'),
)
SEXO = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)
ANUNCIO = (
    ('1', 'Hoteles'),
    ('2', 'Restaurant'),
    ('3', 'Movilidades'),
    ('4', 'Lugares Turisticos'),
)
class UserProfile(models.Model):
    tipo = models.CharField(max_length=1, verbose_name='Tipo',choices=TIPOS,null=False)
    n_trans = models.CharField(max_length=20, verbose_name='N Transaccion',unique=True,error_messages={'unique': 'Ya forma parte del X Coreisc. Te esperamos'})#revisar n de transsaccion longitud
    fecha_trans = models.DateTimeField(auto_now_add=True)#quitar auto_now_add=True solo de prueba
    avatar = models.ImageField("Profile Pic", upload_to="thum/", blank=True, null=True, default="thum/demo.jpg")
    user = models.ForeignKey(User,unique=True)
    user2 = models.CharField(max_length=12,blank=True)
    dni = models.CharField(max_length=8, null=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO,null=False)
    active = models.BooleanField("User Activo",default=False)
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

class Patrocina(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=1, verbose_name='Tipo',choices=ANUNCIO,null=False)
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

class Follow(models.Model):
    user1 = models.ForeignKey(User,related_name="user_sigue")#usuario que sigue
    user2 = models.ForeignKey(User,related_name="user_seguido")#usuario a quien sigue
    def __unicode__(self):
        return self.user1

def create_user_profile(sender, **kwargs):
    """When creating a new user, make a profile for him."""
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)