from django import template
from django.conf import settings
from leave_application.models import Leave, CurrentLeaveRequest, LeaveRequest


register = template.Library()


def get_leave_request(object, user):
    """
    Retrieves list of posts and renders
    The appropriate template to view it
    """
    
    return {
            'req':object,
            'user':user,
            }


def get_processed_request(object, user):
    return {
        'preq':object,
        'user':user,
    }

def get_leave(object, user):
    """
    Retrieves list of posts and renders
    The appropriate template to view it
    """
    
    return {
            'leave':object,
            'user':user,
            }


register.inclusion_tag('leave_application/tags/get_leave.html')(get_leave)
register.inclusion_tag('leave_application/tags/processed_request.html')(get_processed_request)
register.inclusion_tag('leave_application/tags/leave_request.html')(get_leave_request)
