from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..Tools.models import User

from .forms import Login, UserEditor, LoggedIn


def login(request):
	if 'username' in request.session:
		return HttpResponseRedirect('/user')
	if request.method == 'POST':
		form = Login(request.POST)
		if form.is_valid():
			user = User.get_user_by_username(request.POST['username'])
			if user != False and user.password == request.POST['password']:
				for key in user.__dict__:
					if key != '_state':
						request.session[key] = user.__dict__[key]
				return HttpResponseRedirect("/user")
			return HttpResponse("Invalid username/password")

               
	form = Login()
	html = render(request, 'login.html', {'form':form})
	return HttpResponse(html)




def register(request):
	form = UserEditor()
	if request.method == 'POST':
		form = UserEditor(request.POST)
		if form.is_valid():
			user = User.get_user_by_username(request.POST['username'])
			if user != False:
				return HttpResponse("This is an existing username!")
			else:
				User.create_new_user(request.POST['username'], request.POST['password'], request.POST['areaCode'], request.POST['email'], request.POST['phoneNumber'])
			request.session['username'] = request.POST['username']
			return HttpResponseRedirect('/user')
	html = render(request, 'userEditor.html', {"action":"Register!", "form":form})
	return HttpResponse(html)


def user_page(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
	html = render(request, 'user_homepage.html', {"username": request.session['username']})
	return HttpResponse(html)

def logout(request):
	request.session.flush()
	return HttpResponseRedirect('/')


# Create your views here.
