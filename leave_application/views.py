from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from leave_application.forms import (FacultyLeaveForm,
                                     StaffLeaveForm,
                                     StudentLeaveForm,)

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
        form = self.get_form(request)
        if form.is_valid():
            pass
            #TODO: add the logic for handling and saving data to base
        else:
            return render(request, 'leave_application/apply_for_leave.html', {'form': form})

    def get_user_type(self, request):
        return request.user.extrainfo.user_type

    def get_form(self, request):

        user_type = self.get_user_type(request)

        if user_type == 'faculty':
            form = FacultyLeaveForm(initial={})
        elif user_type == 'staff':
            form = StaffLeaveForm(initial={})
        else:
            form = StudentLeaveForm(initial={})

        return form
