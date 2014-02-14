from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from forms import UserEditor, Login, LoggedIn
from django.http import HttpResponseRedirect
from django.shortcuts import render
from tools.models import User

def userEditor(request):
	form = UserEditor()
	if request.method == 'POST':
		form = UserEditor(request.POST)
		if form.is_valid():
			userExists, user = findUser(request.POST['username'])
			if userExists:
				if user.password != request.POST['password']:
					return HttpResponse("This is an existing username and it has a different password than the one you entered!")
				user.areaCode = request.POST['areaCode']
			else:
				user = User(username=request.POST['username'], password=request.POST['password'], areaCode=request.POST['areaCode'])
			user.save()
			request.session['username'] = user.username
			return HttpResponseRedirect('/loggedIn')
	html = render(request, 'userEditor.html', {"action":"Register!", "form":form})
	return HttpResponse(html)


def login(request):
	if 'username' in request.session:
		return HttpResponseRedirect('/loggedIn')
	if request.method == 'POST':
		form = Login(request.POST)
		if form.is_valid():
			userExists, user = findUser(request.POST['username'])
			if userExists:
				if user.password == request.POST['password']:
					request.session['username'] = user.username
					return HttpResponseRedirect("/loggedIn")
		return HttpResponse("Invalid username/password")
			

	form = Login()
	html = render(request, 'login.html', {'form':form})
	return HttpResponse(html)


def loggedIn(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/login')
	if request.method == 'POST':
		del request.session['username']
		return HttpResponseRedirect('/')
	form = LoggedIn()
	html = render(request, 'loggedIn.html', {'username':request.session['username'], 'form':form})
	return HttpResponse(html)


def findUser(username):
	try:
		user = User.objects.get(username=username)
		return True, user
	except:
		return False, {}
