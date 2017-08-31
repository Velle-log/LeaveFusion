from django.conf.urls import url, include
from calender.views import Holidays

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^holidays', login_required(Holidays.as_view()), name='get_holidays'),
]
