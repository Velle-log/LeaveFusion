from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.models import User


# Create your views here.
def handler404(request):
  return render(request, '500.html')


def handler500(request):
  response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
  response.status_code = 500
  return response


@login_required(login_url='/accounts/login/')
def index(request):
	return render(request, 'index/home.html', {'title':'Home'})


@login_required(login_url='/accounts/login/')
def profile_view(request, id):
  user = get_object_or_404(User, id=id)                           #TODO: raise an http404 exception so to reach the 404 page
  return render(request, 'user_app/profile.html', {'title':user.username, 'user': user})
