from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
	return render(request, 'index/home.html', {'title':'Home'})


@login_required(login_url='/accounts/login/')
def profile_view(request):
	return render(request, 'index/profile.html', {'title':request.user.username})
	

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