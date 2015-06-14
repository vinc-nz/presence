from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.authtoken import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'presence.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    
    url(r'^admin', include(admin.site.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^gates/(?P<gate_name>\w{0,50})/$', 'gatecontrol.views.gatecontrol', name='control'),
    url(r'^gates/$', 'gatecontrol.views.get_all_states', name='gates'),
    url(r'^requests/(?P<gate_name>\w{0,50})/$', 'gatecontrol.views.show_requests', name='requests'),
    url(r'^about/$', 'hlcs.views.about', name='about'),
    url(r'^$', 'hlcs.views.homepage', name='home'),
)
