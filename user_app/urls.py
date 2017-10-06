from django.conf.urls import url, include
from user_app import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^profile/(?P<id>[0-9]+)/', views.profile_view, name='profile'),
    url(r'^edit-info/', views.edit_info, name='edit_info'),
    url(r'^logout/', views.logout, name='logout'),
]
