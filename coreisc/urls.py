from django.conf.urls import patterns, include, url
from app.views import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index),
    url(r'^pages/$', allpages),
    url(r"^pages/(\d+)/$", pages),
    url(r"^auspicio/$", allpages),
    url(r"^auspicio/(\d+)/$", auspicio),
    url(r'^login/$', auth_view),
    url(r'^logout/$', logout),
 	url(r'^media/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}),
 	url(r'^accounts/', include('registration.urls')),
    #url(r'^accounts/(?P<username>[a-zA-Z0-9_.-]+)/$', profile),
    url(r"^remove/event/(\d+)/$", removeEvent),
    url(r"^remove/auspicio/(\d+)/$", removePubli),
    url(r"^remove/post/(\d+)/$", removePost),
    url(r"^add/event/(\d+)/$", addEvent),
    url(r"^add/auspicio/(\d+)/$", addPubli),
    url(r'^admin/', include(admin.site.urls)),
)
