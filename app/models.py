# -*- encoding: utf-8 -*-
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
UNIVERSIDADES = (
    ('1', 'Universidad Nacional Pedro Ruiz Gallo'),
    ('2', 'Universidad Alas Peruanas'),
    ('3', 'Universidad Andina del Cusco'),
    ('4', 'Universidad Andina Néstor Cáceres Velásquez'),
    ('5', 'Universidad Antonio Ruiz de Montoya'),
    ('6', 'Universidad Católica de Santa María'),
    ('7', 'Universidad Católica Los Angeles de Chimbote'),
    ('8', 'Universidad Católica San Pablo'),
    ('9', 'Universidad Católica Santo Toribio de Mogrovejo'),
    ('10', 'Universidad Católica Sedes Sapientiae'),
    ('11', 'Universidad César Vallejo'),
    ('12', 'Universidad Científica del Perú'),
    ('13', 'Universidad Científica del Sur'),
    ('14', 'Universidad Continental de Ciencias e Ingeniería'),
    ('15', 'Universidad de Chiclayo'),
    ('16', 'Universidad de Lima'),
    ('17', 'Universidad de Piura'),
    ('18', 'Universidad de San Martín de Porres'),
    ('19', 'Universidad del Pacífico'),
    ('20', 'Universidad ESAN'),
    ('21', 'Universidad Femenina del Sagrado Corazón'),
    ('22', 'Universidad Inca Garcilaso de la Vega'),
    ('23', 'Universidad Marcelino Champagnat'),
    ('24', 'Universidad Nacional Agraria de la Selva'),
    ('25', 'Universidad Nacional Agraria la Molina'),
    ('26', 'Universidad Nacional Daniel Alcides Carrión'),
    ('27', 'Universidad Nacional de Cajamarca'),
    ('28', 'Universidad Nacional de Educación Enrique Guzmán y Valle'),
    ('29', 'Universidad Nacional de Huancavelica'),
    ('30', 'Universidad Nacional de Ingeniería'),
    ('31', 'Universidad Nacional de la Amazonía Peruana'),
    ('32', 'Universidad Nacional de Piura'),
    ('33', 'Universidad Nacional de San Agustin'),
    ('34', 'Universidad Nacional de San Antonio Abad del Cusco'),
    ('35', 'Universidad Nacional de San Cristóbal de Huamanga'),
    ('36', 'Universidad Nacional de San Martín'),
    ('37', 'Universidad Nacional de Trujillo'),
    ('38', 'Universidad Nacional de Tumbes'),
    ('39', 'Universidad Nacional de Ucayali'),
    ('40', 'Universidad Nacional del Altiplano'),
    ('41', 'Universidad Nacional del Callao'),
    ('42', 'Universidad Nacional del Centro del Perú'),
    ('43', 'Universidad Nacional del Santa'),
    ('44', 'Universidad Nacional Federico Villarreal'),
    ('45', 'Universidad Nacional Hermilio Valdizán'),
    ('46', 'Universidad Nacional Jorge Basadre Grohmann'),
    ('47', 'Universidad Nacional José Faustino Sánchez Carrión'),
    ('48', 'Universidad Nacional Mayor de San Marcos'),
    ('49', 'Pontificia Universidad Católica del Perú'),
    ('50', 'Universidad Nacional San Luis Gonzaga de Ica'),
    ('51', 'Universidad Nacional Santiago Antunez de Mayolo'),
    ('52', 'Universidad Peruana Cayetano Heredia'),
    ('53', 'Universidad Peruana de Ciencias Aplicadas'),
    ('54', 'Universidad Peruana los Andes'),
    ('55', 'Universidad Peruana Unión'),
    ('56', 'Universidad Privada Antenor Orrego'),
    ('57', 'Universidad Privada de Tacna'),
    ('58', 'Universidad Privada del Norte'),
    ('59', 'Universidad Privada Norbert Wiener'),
    ('60', 'Universidad Privada San Juan Bautista'),
    ('61', 'Universidad Privada San Pedro'),
    ('62', 'Universidad Ricardo Palma'),
    ('63', 'Universidad San Ignacio de Loyola'),
    ('64', 'Universidad Señor de Sipán'),
    ('65', 'Universidad Tecnológica del Perú'),
)
ALERTAS =(
    ('success','Éxito'),
    ('info','Información'),
    ('warning','Advertencia'),
    ('danger','Urgente'),
)
class UserProfile(models.Model):
    tipo = models.CharField(max_length=1, verbose_name='Tipo',choices=TIPOS,null=False)
    n_trans = models.CharField(max_length=20, verbose_name='N Transaccion',unique=True,error_messages={'unique': 'Ya forma parte del X Coreisc. Te esperamos'})#revisar n de transsaccion longitud
    fecha_trans = models.DateTimeField(auto_now_add=True)#quitar auto_now_add=True solo de prueba
    avatar = models.ImageField("Profile Pic", upload_to="thum/", blank=True, null=True, default="thum/demo.jpg")
    user = models.ForeignKey(User,unique=True)
    uni = models.CharField(max_length=2, verbose_name='Universidad',choices=UNIVERSIDADES,null=False)
    dni = models.CharField(max_length=8, null=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    telefono = models.CharField(max_length=15, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO,null=False)
    #active = models.BooleanField("User Activo",default=False)
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
    def __unicode__(self):
        return self.nombre

class Post(models.Model):
    asistente = models.ForeignKey(User)
    body = models.TextField(max_length=300,verbose_name='Comenta esta publicacion',blank=True)
    event = models.ForeignKey(Events)
    time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return unicode(self.asistente)

class Follow(models.Model):
    user1 = models.ForeignKey(User,related_name="user_sigue")#usuario que sigue
    user2 = models.ForeignKey(User,related_name="user_seguido")#usuario a quien sigue
    def __unicode__(self):
        return self.user1

class Alertas(models.Model):
    tipo    = models.CharField(max_length=7,choices=ALERTAS,blank=True,default="info")
    usuario = models.ForeignKey(User)
    mensaje = models.TextField(verbose_name='Mensaje')
    visto = models.BooleanField("Leido",default=False)
    def __unicode__(self):
        return unicode(self.usuario)

def create_user_profile(sender, **kwargs):
    """When creating a new user, make a profile for him."""
    u = kwargs["instance"]
    if not UserProfile.objects.filter(user=u):
        UserProfile(user=u).save()

post_save.connect(create_user_profile, sender=User)