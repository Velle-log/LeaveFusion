from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    DAY_TYPE = (
        ('working', 'Working Day'),
        ('holiday', 'Holiday'),
        ('restricted', 'Restricted Holiday')
    )

    date = models.DateField()
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    type_of_event = models.CharField(max_length=20, choices=DAY_TYPE)

    def __str__(self):
        return '{}: {}'.format(self.date, self.name)


#TODO: Add attendence to each subject
"""
class Attendence(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

"""
