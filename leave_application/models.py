from django.db import models
from django.contrib.auth.models import User
from user_app.models import ExtraInfo
from .helpers import count_work_days

from django.dispatch import receiver
# Create your models here.

class Constants:
    LEAVE_TYPE = (
        ('casual', 'Casual Leave'),
        ('restricted', 'Restricted Holidays'),
        ('vacation', 'Vacation Leave'),
        ('commuted', 'Commuted Leave'),
        ('earned', 'Earned Leave'),
        ('special_casual', 'Special Casual Leave'),
    )

class LeavesCount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    casual = models.IntegerField(default=8)
    special_casual = models.IntegerField(default=15)
    restricted = models.IntegerField(default=2)
    commuted = models.IntegerField(default=20)
    earned = models.IntegerField(default=30)
    vacation = models.IntegerField(default=60)

    def __str__(self):
        return 'user: {}'.format(self.user.username)

@receiver(models.signals.post_save, sender=ExtraInfo)
def create_leaves_count(instance, created, **kwargs):
    if created:
        if instance.user_type != 'student':
            LeavesCount.objects.create(user = instance.user)


class Leave(models.Model):
    # TODO: Add required fields
    applicant = models.ForeignKey(User,
                                  related_name='leave_applications',
                                  on_delete=models.CASCADE)
    type_of_leave = models.CharField(max_length=20,
                                  choices=Constants.LEAVE_TYPE,
                                  default='casual')
    academic_replacement = models.ForeignKey(User,
                                             related_name='acad_rep_for',
                                             null=True, on_delete=models.CASCADE)
    administrative_replacement = models.ForeignKey(User,
                                                   related_name='admin_rep_for',
                                                   null=True, on_delete=models.CASCADE)
    acad_done = models.BooleanField(default=True)
    admin_done = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    purpose = models.CharField(max_length=1000, blank=False, default='No Purpose')
    leave_address = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=10, blank=False, default='processing')
    station = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    @property
    def count_work_days(self):
        """
            property which returns the workdays in the leave period
            ==> Actual considered leave days
        """
        return count_work_days(self.start_date, self.end_date)

    @property
    def get_year(self):
        return self.start_date.strftime('%Y')

    def __str__(self):
        return 'By: {}, type: {}'.format(self.applicant.username, self.type_of_leave)

class CurrentLeaveRequest(models.Model):

    from user_app.models import Designation

    applicant = models.ForeignKey(User,
                                  related_name='cur_leave_requests',
                                  on_delete=models.CASCADE)
    requested_from = models.ForeignKey(User,
                                       related_name='cur_received_requests',
                                       on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Designation, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leave, related_name='cur_requests', on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, default='other')
    station = models.BooleanField(default=False)
    def __str__(self):
        return '{} requested from {}'.format(self.applicant.username, self.requested_from.username)

class LeaveRequest(models.Model):
    from user_app.models import Designation

    applicant = models.ForeignKey(User,
                                  related_name='leave_requests',
                                  on_delete=models.CASCADE)
    requested_from = models.ForeignKey(User,
                                       related_name='received_requests',
                                       on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Designation, on_delete=models.CASCADE)
    leave = models.ForeignKey(Leave, related_name='requests', on_delete=models.CASCADE)
    # both = models.BooleanField(default=False)
    remark = models.CharField(max_length=200, blank=False, default='')
    status = models.BooleanField(default=False)
    station = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} requested from {}, status: {}'.format(self.applicant.username,
                                                         self.requested_from.username,
                                                         self.status)

@receiver(models.signals.post_save, sender=Leave)
def add_current_leave_request(instance, sender, created, **kwargs):
    if created:
        acad_rep = instance.academic_replacement
        admin_rep = instance.administrative_replacement
        if acad_rep is not None or admin_rep is not None:
            if acad_rep is not None:
                CurrentLeaveRequest.objects.create(
                    applicant = instance.applicant,
                    requested_from = acad_rep,
                    position = acad_rep.extrainfo.designation,
                    leave = instance,
                    permission = 'academic',
                )
            if admin_rep is not None:
                CurrentLeaveRequest.objects.create(
                    applicant = instance.applicant,
                    requested_from = admin_rep,
                    position = admin_rep.extrainfo.designation,
                    leave = instance,
                    permission = 'admin',
                )
        else:
            sanc_auth = instance.applicant.extrainfo.sanctioning_authority
            req_user = sanc_auth.holds_designation.first().user
            CurrentLeaveRequest.objects.create(
                applicant = instance.applicant,
                requested_from = req_user,
                position = sanc_auth,
                leave = instance,
            )
