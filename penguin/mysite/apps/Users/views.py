from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import User

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
				new_user = User.create_new_user(request.POST['username'], request.POST['password'], request.POST['area_code'], request.POST['email'], request.POST['phone_number'], request.POST['default_pickup_arrangements'])
			request.session.clear()
			for user_attribute in new_user.__dict__:
#				print(user_attribute)
				if user_attribute != '_state':
					request.session[user_attribute] = new_user.__dict__[user_attribute]
#			print('username' in request.session)
#			print('default_pickup_arrangements' in request.session)
			return HttpResponseRedirect('/user')
	html = render(request, 'userEditor.html', {"action":"Register!", "form":form})
	return HttpResponse(html)



def user_editor(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
	form = UserEditor(initial={'username': request.session['username'], 'email': request.session['email'], 'area_code': request.session['area_code'], 'phone_number': request.session['phone_number'], 'default_pickup_arrangements': request.session['default_pickup_arrangements']})
	form.disable_register_things()
	if request.method == 'POST':

#		form = UserEditor(request.POST)
#		if form.is_valid():

#		print(request.POST)
		User.update_user(request.session['username'], request.POST['password'], request.POST['phone_number'], request.POST['area_code'], request.POST['email'], request.POST['default_pickup_arrangements'])
		request.session['password'] = request.POST['password']
		request.session['phone_number'] = request.POST['phone_number']
		request.session['area_code'] = request.POST['area_code']
		request.session['email'] = request.POST['email']
		request.session['default_pickup_arrangements'] = request.POST['default_pickup_arrangements']
		return HttpResponseRedirect('/user')
#User.
	html = render(request, 'userEditor.html', {"action" : "Save!", "form": form})
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
