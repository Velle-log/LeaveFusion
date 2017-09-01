from django.conf.urls import url, include
from user_app import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/', views.profile_view, name='profile_view'),
    url(r'^edit-info/', views.edit_info, name='edit_info'),
]
