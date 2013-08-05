from app.models import *
from django.contrib import admin

class PonenteAdmin(admin.ModelAdmin):
    list_display = ('ponente_thumb','nombre', 'body')
class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'fecha', 'ponente','banner')
admin.site.register(Ponente,PonenteAdmin)
admin.site.register(Events,EventsAdmin)