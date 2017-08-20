from django.db import models
from django.contrib.auth.models import User
from .helpers import count_work_days
from user_app.models import Designation
# Create your models here.

class Constants:
    LEAVE_TYPE = (
        ('casual', 'Casual Leave'),
        ('restricted', 'Restricted Leave'),
        ('station', 'Station Leave'),
        ('vacation', 'Vacation Leave'),
        ('earned', 'Earned Leave'),
        ('special_casual', 'Special Casual Leave'),
    )

class Leave(models.Model):
    # TODO: Add required fields
    applicant = models.ForeignKey(User,
                                  related_name='leave_applications',
                                  on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20,
                                  choices=Constants.LEAVE_TYPE,
                                  default='casual')
    academic_replacement = models.ForeignKey(User,
                                             related_name='acad_rep_for',
                                             null=True, on_delete=models.CASCADE)
    administrative_replacement = models.ForeignKey(User,
                                                   related_name='admin_rep_for',
                                                   null=True, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    purpose = models.CharField(max_length=1000, blank=False, default='No Purpose')
    leave_address = models.CharField(max_length=100, blank=True, default='')

    @property
    def count_leave_days(self):
        """
            property which returns the workdays in the leave period
            ==> Actual considered leave days
        """
        return count_work_days(self.start_date, self.end_date)

class LeaveRequest(models.Model):
    # TODO: Add required fields
    applicant = models.ForeignKey(User,
                                  related_name='leave_requests',
                                  on_delete=models.CASCADE)
    requested_from = models.ForeignKey(User,
                                       related_name='received_requests',
                                       on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Designation, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leave, related_name='requests', on_delete=models.CASCADE)
    remark = models.CharField(max_length=200, blank=False)
    processed = models.BooleanField(default=False)

class CurrentLeaveRequest(LeaveRequest):
    pass
