from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'presence.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^open', 'selfopen.views.wait_ring', name='open'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^', 'checker.views.door_status', name='status')
)
