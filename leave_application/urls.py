from django.conf.urls import url, include
from leave_application.views import ApplyLeave, GetApplications, ProcessRequest, GetLeaves
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^apply', login_required(ApplyLeave.as_view()), name='apply_for_leave'),
    url(r'^getapplications', login_required(GetApplications.as_view()), name='get_applications'),
    url(r'^get-leaves/', login_required(GetLeaves.as_view()), name='get_leaves'),
    url(r'^process-request/(?P<id>[0-9]+)/', login_required(ProcessRequest.as_view()), name='process_request'),
]
