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
admin.site.register(Ponente,PonenteAdmin)
admin.site.register(Events,EventsAdmin)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Publicidad, PublicidadAdmin)