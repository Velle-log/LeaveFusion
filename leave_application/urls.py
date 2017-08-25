from django.conf.urls import url, include
from leave_application.views import ApplyLeave
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^apply', login_required(ApplyLeave.as_view()), name='apply_for_leave'),
]
