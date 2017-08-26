def count_work_days(start_date, end_date):
    pass

class FormData:

    def __init__(self, request, leave_request):
        self.request = request
        self.leave_request = leave_request

    @property
    def forward(self):
        sanc_auth = self.leave_request.applicant.department.sanctioning_authority
        sanc_officer = self.leave_request.applicant.department.sanctioning_officer
        type_of_leave = self.leave_request.leave.type_of_leave

        designation = self.request.user.designation

        if sanc_auth == sanc_officer and designation == sanc_auth:
            return False

        elif sanc_auth == designation and type_of_leave in ['casual', 'restricted'] \
             or self.leave_request.requested_from == self.request.user:

             return True
        else:
            return False
