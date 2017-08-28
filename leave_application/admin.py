from django.contrib import admin
from leave_application.models import (Leave, LeaveRequest,
                                      CurrentLeaveRequest,
                                      LeavesCount)
# Register your models here.

admin.site.register(Leave)
admin.site.register(LeaveRequest)
admin.site.register(CurrentLeaveRequest)
admin.site.register(LeavesCount)
