from django.conf.urls import url, include
from user_app import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/', views.profile_view, name='profile_view'),
]
