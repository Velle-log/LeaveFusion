from django import forms
from leave_application.models import CurrentLeaveRequest, LeavesCount
from django.contrib.auth.models import User
from user_app.models import Administration
from leave_application.helpers import get_object_or_none, count_work_days

import datetime

class LeaveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
    start_date = forms.DateField(widget=forms.SelectDateWidget(), label='From')
    end_date = forms.DateField(widget=forms.SelectDateWidget(), label='Upto')
    leave_address = forms.CharField(label='Leave Address',
                                    widget=forms.TextInput(attrs={
                                                                    'placeholder': 'Address of leave'
                                                                 }
                                                          ),
                                    max_length=100)
    purpose = forms.CharField(label='Purpose', widget=forms.Textarea, max_length=300)

class FacultyLeaveForm(LeaveForm):

    try:
        USER_CHOICES = list((user.username, '{} {}'.format(user.first_name, user.last_name)) \
                             for user in User.objects.all() \
                             if user.extrainfo.user_type == 'faculty')
    except Exception as e:
        USER_CHOICES = []

    from leave_application.models import Constants as cts
    LEAVE_CHOICES = cts.LEAVE_TYPE
    type_of_leave = forms.CharField(widget=forms.Select(choices=LEAVE_CHOICES))
    acad_rep = forms.CharField(label = 'Academic Responsibility Assigned To',
                               widget=forms.Select(choices=USER_CHOICES))
    admin_rep = forms.CharField(label = 'Administrative Responsibility Assigned To',
                                widget=forms.Select(choices=USER_CHOICES))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(FacultyLeaveForm, self).__init__(*args, **kwargs)

        is_administrator = get_object_or_none(Administration, administrator=self.user)

        if not is_administrator:
            self.fields.pop('admin_rep')

    def clean(self):
        admin_rep = self.cleaned_data.get('admin_rep', None)
        acad_rep = self.cleaned_data.get('acad_rep', None)

        if self.user.username in [acad_rep, admin_rep]:
            raise forms.ValidationError('You can not choose yourself as replacement')

        type_of_leave = self.cleaned_data.get('type_of_leave')
        leave_object = LeavesCount.objects.filter(user=self.user).first()
        remaining_leaves = getattr(leave_object, type_of_leave)
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        now = datetime.datetime.now()
        today = datetime.date(now.year, now.month, now.day)
        if start_date > end_date or start_date < today or end_date < today:
            raise forms.ValidationError('Invalid Dates')
        request_leaves = count_work_days(start_date, end_date)

        # TODO: Vacation leaves only in summer vacations
        # TODO: User must not have leaves in between start_date and end_date

        if remaining_leaves < request_leaves:
            raise forms.ValidationError('You have {} remaining {} leaves'.format(remaining_leaves,
                                                                                 type_of_leave))

        return self.cleaned_data


class StaffLeaveForm(LeaveForm):
    try:
        USER_CHOICES = tuple((user.username, user.username) \
                              for user in User.objects.all() \
                              if user.extrainfo.user_type == 'staff')
    except:
        USER_CHOICES = []
    from leave_application.models import Constants as cts
    LEAVE_CHOICE = cts.LEAVE_TYPE
    type_of_leave = forms.CharField(widget=forms.Select(choices=LEAVE_CHOICE))
    admin_rep = forms.CharField(label='Administrative Responsibility Assigned To',
                                widget=forms.Select(choices=USER_CHOICES))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(StaffLeaveForm, self).__init__(*args, **kwargs)

        # is_administrator = get_object_or_none(Administration, administrator=self.user)
        #
        # if not is_administrator:
        #     self.fields.pop('admin_rep')

    def clean(self):
        pass
        #TODO: add validation of forms

class StudentLeaveForm(LeaveForm):

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')

        super(StudentLeaveForm, self).__init__(*args, **kwargs)

    def clean(self):
        pass
        #TODO: add validation
