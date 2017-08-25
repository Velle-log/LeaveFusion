from django.conf.urls import url, include
from user_app import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
]
