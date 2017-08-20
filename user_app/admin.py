from django.contrib import admin
from .models import (ExtraInfo, Designation,
                     DepartmentInfo, Administration,)
# Register your models here.
admin.site.register(ExtraInfo)
admin.site.register(Designation)
admin.site.register(DepartmentInfo)
admin.site.register(Administration)
