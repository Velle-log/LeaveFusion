from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from  django.http import Http404
from django.contrib.auth.models import User


# Create your views here.
def handler404(request):
  response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
  response.status_code = 404
  return response


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
  try:
    user = User.objects.get(id = id)
  except:
    return Http404('Page not found :/')                               #TODO: raise an http404 exception so to reach the 404 page
  return render(request, 'user_app/profile.html', {'title':user.username, 'user': user})
