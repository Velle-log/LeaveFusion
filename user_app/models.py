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


class Designation(models.Model):
    name = models.CharField(max_length=20, unique=True, blank=False)

    def __str__(self):
        return self.name

class DepartmentInfo(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return 'department: {}'.format(self.name)

class ExtraInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='holds_designation', null=True)
    user_type = models.CharField(max_length=20, default='student')
    unique_id = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=2, choices=Constants.SEX_CHOICES, default='M')
    department = models.ForeignKey(DepartmentInfo, on_delete=models.CASCADE, null=True)
    profile_picture = models.ImageField(null=True, blank=True)
    about_me = models.TextField(default='', max_length=1000, blank=True)
    # TODO: Remove this and add to another model
    sanctioning_authority = models.ForeignKey(Designation,
                                              related_name='sanctioning_auth',
                                              on_delete=models.CASCADE, null=True, blank=True)
    sanctioning_officer = models.ForeignKey(Designation, related_name='sanctioning_officer', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def is_onleave(self):
        from django.db.models import Q
        from leave_application.models import Leave
        now = datetime.date.today()
        leave = Leave.objects.filter(Q(applicant = self.user) \
                                     & Q(start_date__gte = now) & Q(end_date__lte = now) \
                                     & ~Q(status = 'rejected'))

        return True if leave else False

    def __str__(self):
        return '{} type is {}'.format(self.user.username, self.user_type)

@receiver(models.signals.post_save, sender=User)
def add_extra_info(sender, instance, created, **kwargs):
    if created:
        ExtraInfo.objects.create(user=instance)
        #TODO: Add automatic creation of LeavesCount if user_type is not student

# TODO: Remove this.
class Administration(models.Model):
    administrator = models.OneToOneField(User, related_name='administration_duty',
                                         on_delete=models.CASCADE)
    position = models.OneToOneField(Designation, on_delete=models.CASCADE)

    def __str__(self):
        return '{} at position {}'.format(self.administrator.username, self.position)

# TODO: Put it in leave_application app.
class Replacement(models.Model):

    CHOICES = [
        ('academic', 'Academic Replacement'),
        ('administrative', 'Administrative Replacement'),
    ]

    replacee = models.ForeignKey(User, related_name='replacements', on_delete=models.CASCADE)
    replacer = models.ForeignKey(User, related_name='replacing', on_delete=models.CASCADE)
    replacement_type = models.CharField(max_length=20, choices=CHOICES, default='academic')

    def __str__(self):
        return '{}: {} replaces {}'.format(self.replacement_type, self.replacer, self.replacee)


"""
from django.contrib.auth.models import User; User.objects.all()[0].delete();
"""
