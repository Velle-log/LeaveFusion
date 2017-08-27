from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
	return render(request, 'index/home.html', {'title':'Home'})


@login_required(login_url='/accounts/login/')
def profile_view(request):
	return render(request, 'index/profile.html', {'title':request.user.username})
