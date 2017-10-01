from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404
from .models import ExtraInfo
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from PIL import Image
from django.contrib import messages
from django.core.urlresolvers import reverse

from datetime import date
import datetime
from user_app.models import Replacement

from leave_application.models import LeaveMigration, MigrationChangeDate
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
    	return redirect(reverse('profile:profile_view', args=[request.user.id]))
    return render(request, 'user_app/user_form.html', { 'user':request.user, 'title': 'Profile', 'action':'Edit-Profile' })

# @login_required(login_url='/accounts/login/')
def index(request):
    if request.user.is_authenticated():
        make_migrations()
        return render(request, 'fusion/dashboard/dashboard.html', {'title':'Home'})
    return render(request, 'fusion/general/index1.html')

@login_required(login_url='/accounts/login/')
def profile_view(request, id):
    #TODO: raise an http404 exception so to reach the 404 page
    user = get_object_or_404(User, id=id)
    name = user.first_name+" "+user.last_name
    return render(request, 'user_app/profile.html', {'title':name, 'user': user})


def make_migrations():
    today = date.today()
    last_date = MigrationChangeDate.objects.all().first()

    if today > last_date.last_date_change:
        data_to_delete = LeaveMigration.objects.filter(end_date__lte=today)

        for migration in data_to_delete:
            if migration.type == 'add':
                migration.delete()
            else:
                migration.rep.delete()

        data = LeaveMigration.objects.filter(start_date__lte=today)

        for migration in data:
            if migration.type == 'add':
                rp = Replacement.objects.create(
                    replacee = migration.replacee,
                    replacer = migration.replacer,
                    replacement_type = migration.replacement_type
                )

                LeaveMigration.objects.create(
                    type = 'del',
                    start_date = migration.end_date + datetime.timedelta(days=1),
                    replacer = migration.replacer,
                    replacee = migration.replacee,
                    rep = rp,
                )
                migration.delete()
            else:
                migration.rep.delete()
        last_date.last_date_change = today
        last_date.save()
