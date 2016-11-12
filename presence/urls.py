from django.conf.urls import patterns, include, url
from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'presence.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    
    url(r'^admin', include(admin.site.urls)),

    # TODO remove these views
   url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
   url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^about/$', 'hlcs.views.about', name='about'),
    url(r'^$', 'hlcs.views.homepage', name='home'),
)
