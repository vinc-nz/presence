from django.conf.urls import patterns, include, url
from django.contrib import admin

from gatecontrol import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'presence.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    
    url(r'^admin', include(admin.site.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token)
)
