import datetime

def count_work_days(start_date, end_date):
    days = (end_date - start_date).days + 1
    weekends = 0
    for _ in range(days):
        if (start_date + datetime.timedelta(days = _)).weekday in [5, 6]:
            weekends += 1
    return days - weekends

def get_object_or_none(cls, **kwargs):
    # for key, value in kwargs.items():
    #     print('{} ==> {}'.format(key, value))
    try:
        return cls.objects.get(**kwargs)
    except:
        return None

class FormData:

    def __init__(self, request, leave_request):
        self.request = request
        self.leave_request = leave_request

    @property
    def forward(self):
        sanc_auth = self.leave_request.applicant.extrainfo.department.sanctioning_authority
        sanc_officer = self.leave_request.applicant.extrainfo.department.sanctioning_officer
        type_of_leave = self.leave_request.leave.type_of_leave

        designation = self.request.user.extrainfo.designation
        should_forward = False
        #if sanc_auth == sanc_officer and designation == sanc_auth:
        #    should_forward = False

        if sanc_auth == designation and type_of_leave not in ['casual', 'restricted'] \
             or self.leave_request.requested_from != self.request.user:

             should_forward = True
        #else:
        #    return False
        print(should_forward)
        return should_forward
