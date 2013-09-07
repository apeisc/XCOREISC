from django.conf.urls import patterns, include, url
from app.views import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
    url(r'^eventos/$', allpages),
    url(r"^evento/(\d+)/$", pages),
    url(r"^auspicio/$", allpages),
    url(r"^planifica/$", planifica),
    url(r"^auspicio/(\d+)/$", auspicio),
    url(r'^login/$', auth_view),
    url(r'^logout/$', logout),
 	url(r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}),
 	#url(r'^accounts/', include('registration.urls')),sin uso por ahora
    url(r'^miembro/(?P<username>[a-zA-Z0-9_.-]+)/$', account),
    url(r'^follow/(?P<username>[a-zA-Z0-9_.-]+)/$', follow),
    url(r'^nofollow/(?P<username>[a-zA-Z0-9_.-]+)/$', nofollow),
    #url(r'^accounts/(?P<username>[a-zA-Z0-9_.-]+)/$', profile),
    url(r"^remove/event/(\d+)/$", removeEvent),
    url(r"^remove/auspicio/(\d+)/$", removePubli),
    url(r"^remove/post/(\d+)/$", removePost),
    url(r"^add/event/(\d+)/$", addEvent),
    url(r"^add/auspicio/(\d+)/$", addPubli),
    url(r'^edit_profile/', edit_user),
    url(r'^checkuser/', checkUser),
    url(r'^checktrans/', checkTrans),
    url(r'^checkemail/', checkEmail),
    url(r'^process/$', process),
    #url(r'^posting/$', posting),
    url(r'^process/create/', new_user),
    url(r'^alerta/(\d+)/$',alert),
    url(r'^notificar/(?P<username>[a-zA-Z0-9_.-]+)/$',Notificar),
    url(r'^admin/', include(admin.site.urls)),
)
