from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404
from .models import ExtraInfo
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from PIL import Image
from django.contrib import messages

# Create your views here.
def handler404(request):
  return render(request, '500.html')


def handler500(request):
  response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
  response.status_code = 500
  return response

@login_required(login_url='/accounts/login/')
def edit_info(request):
	if request.method == 'POST':
		user_details = request.user.extrainfo
		if request.POST.get('remove'):
			user_details.profile_picture.delete(save=False)
		if request.FILES.get('profile_picture'):
			img = request.FILES.get('profile_picture')
			try:
				im = Image.open(img)
			except Exception as e:
				print(e)
				error = "You didn't upload a image file or the format of image file is not supported !"
				return render(request, 'user_app/user_form.html', { 'user':request.user, 'title': 'Profile', 'action':'Edit-Profile', 'error':error })
			user_details.profile_picture.delete(save=False)
			user_details.profile_picture = request.FILES.get('profile_picture')
		user_details.about_me = request.POST.get('about_me')
		user_details.save()
		messages.success(request, ('Your profile was successfully updated!'))
		return redirect('/')
	return render(request, 'user_app/user_form.html', { 'user':request.user, 'title': 'Profile', 'action':'Edit-Profile' })

@login_required(login_url='/accounts/login/')
def index(request):
	return render(request, 'index/home.html', {'title':'Home'})


@login_required(login_url='/accounts/login/')
def profile_view(request, id):
  user = get_object_or_404(User, id=id)                           #TODO: raise an http404 exception so to reach the 404 page
  name = user.first_name+" "+user.last_name
  return render(request, 'user_app/profile.html', {'title':name, 'user': user})
