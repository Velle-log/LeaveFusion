from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from user_app.views import index

urlpatterns = [
	url(r'^$', index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^leave/', include('leave_application.urls', namespace='leave_application')),
    url(r'^profile/', include('user_app.urls', namespace='profile')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
