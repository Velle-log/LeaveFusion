from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponse, Http404
from leave_application.forms import (FacultyLeaveForm,
                                     StaffLeaveForm,
                                     StudentLeaveForm,)

from leave_application.helpers import FormData

class ApplyLeave(View):
    """
        A Class Based View which handles user applying for leave
    """
    def get(self, request):
        """
            view to handle get request to /leave/apply
        """
        form = self.get_form(request)
        return render(request, 'leave_application/apply_for_leave.html', {'form': form})

    def post(self, request):
        """
            view to handle post request to /leave/apply
        """
        form = self.get_form(request, request.POST)
        if form.is_valid():

            try:
                leave_obj = Leave.objects.create(
                    applicant = request.user,
                    leave_type = form.cleaned_data['type_of_leave'],
                    academic_replacement = form.cleaned_data.get('acad_rep', None),
                    administrative_replacement = form.cleaned_data.get('admin_rep', None),
                    purpose = form.cleaned_data.get('purpose', ''),
                    leave_address = form.cleaned_data.get('leave_address', ''),
                    start_date = form.cleaned_data['start_date'],
                    end_date = form.cleaned_data['end_date'],
                )

            except:
                return render(request,
                              'leave_application/apply_for_leave.html',
                              {'form': form, 'message': 'Failed'})
            return render(request, 'leave_application/apply_for_leave', {'message': 'success'})

        else:
            return render(request, 'leave_application/apply_for_leave.html', {'form': form})

    def get_user_type(self, request):
        return request.user.extrainfo.user_type

    def get_form(self, request, initial = {}):

        user_type = self.get_user_type(request)

        if user_type == 'faculty':
            form = FacultyLeaveForm(initial)
        elif user_type == 'staff':
            form = StaffLeaveForm(initial)
        else:
            form = StudentLeaveForm(initial)

        return form


class ProcessRequest(View):

    def get(self, request, id):
        leave_request = get_object_or_404(CurrentLeaveRequest, id=id)
        type_of_leave = leave_request.leave.type_of_leave

        do = request.GET.get('do')
        remark = request.GET.get('remark', '')
        sanc_auth = leave_request.applicant.department.sanctioning_authority
        sanc_officer = leave_request.applicant.department.sanctioning_officer
        designation = request.user.designation

        if do == 'accept':
            if sanc_auth == sanc_officer and designation == sanc_auth:
                self.create_leave_request(leave_request, True, accept=True, remark=remark)

            elif sanc_auth == designation:

                if type_of_leave not in ['casual', 'restricted']:
                    raise Http404

                leave_request = self.create_leave_request(leave_request,
                                                          True, accept=True,
                                                          remark=remark)

            elif sanc_officer == designation:

                self.create_leave_request(leave_request, True, accept=True, remark=remark)

            elif designation == leave_request.position:

                leave_request = self.create_leave_request(leave_request, False, accept=True, remark=remark)
                CurrentLeaveRequest.objects.create(
                    leave = leave_request.leave,
                    requested_from = sanc_auth,
                    applicant = leave_request.applicant,
                    position = sanc_auth,
                )

            else:
                raise Http404

        elif do == 'forward':

            if sanc_auth == sanc_officer and designation == sanc_auth:
                raise Http404

            condition = type_of_leave in ['casual', 'restricted'] \
                        and designation == sanc_auth

            if condition:
                leave_request = self.create_leave_request(leave_request, False, accept=True, remark=remark)
                CurrentLeaveRequest.objects.create(
                    leave = leave_request.leave,
                    requested_from = sanc_officer,
                    applicant = leave_request.applicant,
                    position = sanc_officer,
                )

            else:
                raise Http404

        elif do == 'reject':

            if sanc_auth == sanc_officer and designation == sanc_auth:
                self.create_leave_request(leave_request, True, accept=False, remark=remark)

            if sanc_auth == designation and type_of_leave not in ['casual', 'restricted']:
                raise Http404

            elif designation in [sanc_auth, sanc_officer]:
                leave_request = self.create_leave_request(leave_request,
                                                          False, accept=False,
                                                          remark=remark)
            else:
                leaves_data = leave_request.leave.requests
                for leave in leaves_data:
                    self.create_leave_request(leave, False, accept=False, remark=remark)

        else:
            raise Http404

        return JsonResponse({'message': 'Operation Successful'}, status=200)

    def create_leave_request(cur_leave_request, final, accept=False, remark=''):
        leave_request = LeaveRequest.objects.create(
            leave = cur_leave_request.leave,
            applicant = cur_leave_request.applicant,
            requested_from = cur_leave_request.requested_from,
            remark = remark,
            position = cur_leave_request.position,
            status = accept,
        )

        if not accept and final:
            cur_leave_request.leave.status = 'rejected'
        elif final:
            cur_leave_request.leave.status = 'accepted'

        cur_leave_request.delete()
        return leave_request

class GetApplications(View):

    def get(self, request):

        request_list = map(lambda x: FormData(request, x),
                           CurrentLeaveRequest.objects.filter(requested_from=request.user))
        return render(request, 'leave_application/get_requests.html', {'data': request_list})
