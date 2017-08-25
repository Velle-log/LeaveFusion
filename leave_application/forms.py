from django import forms
from leave_application.models import CurrentLeaveRequest
from django.contrib.auth.models import User

class LeaveForm(forms.Form):

    purpose = forms.CharField(label='Purpose', max_length=300)
    start_date = forms.DateField(widget=forms.SelectDateWidget(), label='From')
    end_date = forms.DateField(widget=forms.SelectDateWidget(), label='Upto')
    leave_address = forms.CharField(label='Leave Address', max_length=100)

class FacultyLeaveForm(LeaveForm):
    USER_CHOICES = tuple((user, user) for user in User.objects.all() if user.extrainfo.user_type == 'faculty')
    from leave_application.models import Constants as cts
    LEAVE_CHOICES = cts.LEAVE_TYPE
    type_of_leave = forms.CharField(widget=forms.Select(choices=LEAVE_CHOICES))
    admin_rep = forms.CharField(label = 'Administrative Responsibility Assigned To',
                                widget=forms.Select(choices=USER_CHOICES))
    acad_rep = forms.CharField(label = 'Academic Responsibility Assigned To',
                               widget=forms.Select(choices=USER_CHOICES))

    def clean(self):
        pass
        #TODO: add validation of forms

class StaffLeaveForm(LeaveForm):
    USER_CHOICES = tuple((user, user) for user in User.objects.all() if user.extrainfo.user_type == 'staff')
    from leave_application.models import Constants as cts
    LEAVE_CHOICE = cts.LEAVE_TYPE
    type_of_leave = forms.CharField(widget=forms.Select(choices=LEAVE_CHOICE))
    admin_rep = forms.CharField(label='Administrative Responsibility Assigned To',
                                widget=forms.Select(choices=USER_CHOICES))

    def clean(self):
        pass
        #TODO: add validation of forms

class StudentLeaveForm(LeaveForm):

    def clean(self):
        pass
        #TODO: add validation
