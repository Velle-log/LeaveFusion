from django.conf.urls import url, include
from user_app import views

urlpatterns = [
    url(r'^$', views.profile_view, name='profile_view'),
]
