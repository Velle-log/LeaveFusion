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
        self.forward = False

    def __str__(self):
        return str(self.leave_request) + ' ' + str(self.forward)
