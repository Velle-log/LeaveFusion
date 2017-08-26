from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver

import datetime

class Constants:
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    RELATIONSHIP = (
        ('single', 'Single'),
        ('married', 'Married')
    )


class Designation(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False)


class DepartmentInfo(models.Model):
    name = models.CharField(max_length=30, unique=True)
    sanctioning_authority = models.ForeignKey(Designation,
                                              related_name='sanctioning_leave_to',
                                              on_delete=models.CASCADE)
    sanctioning_officer = models.ForeignKey(Designation, on_delete=models.CASCADE)


class ExtraInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True)
    user_type = models.CharField(max_length=20, default='student')
    sex = models.CharField(max_length=2, choices=Constants.SEX_CHOICES, default='M')
    relationship_status = models.CharField(max_length=10,
                                           choices=Constants.RELATIONSHIP, default='single')
    department = models.ForeignKey(DepartmentInfo, on_delete=models.CASCADE, null=True)

    @property
    def is_onleave(self):
        from leave_application.models import Leave
        now = datetime.datetime.now()
        leave = Leave.objects.filter(applicant = self.user,
                                     start_date__gte = now, end_date__lte = now,
                                     status = 'accepted')

        return True if leave else False


@receiver(models.signals.post_save, sender=User)
def add_extra_info(sender, instance, created, **kwargs):
    if created:
        ExtraInfo.objects.create(user=instance)
        #TODO: Add automatic creation of LeavesCount if user_type is not student


class Administration(models.Model):
    administrator = models.ForeignKey(User, related_name='administration_duty',
                                            on_delete=models.CASCADE)
    position = models.ForeignKey(Designation, on_delete=models.CASCADE)


"""
from django.contrib.auth.models import User; User.objects.all()[0].delete();
"""
