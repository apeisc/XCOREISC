from app.models import *
from django.contrib import admin
class PostAdmin(admin.ModelAdmin):
    list_display = ["asistente","event","time"]
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
class PonenteAdmin(admin.ModelAdmin):
    list_display = ('ponente_thumb','nombre', 'body')
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'fecha', 'ponente','banner')
class PublicidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'body', 'direccion')
class PaisAdmin(admin.ModelAdmin):
    list_display = ["nombre"]
class AlertasAdmin(admin.ModelAdmin):
    list_display = ["tipo","usuario","mensaje","visto"]
admin.site.register(Ponente,PonenteAdmin)
admin.site.register(Events,EventsAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Patrocina, PublicidadAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Alertas,AlertasAdmin)