from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('user_app.urls', namespace = 'user_app')),
    url(r'^leave/', include('leave_application.urls', namespace='leave_application')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
