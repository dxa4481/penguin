from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..Tools.models import User

from forms import Login, UserEditor, LoggedIn


def login(request):
        if 'username' in request.session:
                return HttpResponseRedirect('/user')
        if request.method == 'POST':
                form = Login(request.POST)
                if form.is_valid():
                        user = User.get_user(request.POST['username'])
			print(user)
                        if userExists:
                                if user.password == request.POST['password']:
                                        request.session['username'] = user.username
                                        return HttpResponseRedirect("/loggedIn")
                return HttpResponse("Invalid username/password")


        form = Login()
        html = render(request, 'login.html', {'form':form})
        return HttpResponse(html)




def register(request):
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

# Create your views here.
