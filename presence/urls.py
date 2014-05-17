from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'presence.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^open', 'selfopen.views.wait_ring', name='open'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^', 'checker.views.door_status', name='status')
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
