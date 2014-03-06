from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CreateTool

from .models import *

# Display a list of tools
def user_tools(request):
	
	#context = {'tool_list': ['hammer','chisel','toothbrush'] }
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
		
	#user_id = request.session['id']
	username = request.session['username']
	user_id = User.get_user_by_username(username).id
	context = { 'tool_list': User.get_all_user_tools(user_id),
				#'tool_list': Tool.objects.all(),
				'username': username,
			  }
	
	return render(request, 'user_tools.html', context)
	#return HttpResponse("This is a test of the User Tools page. Quack.")


def new_tool(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = CreateTool(request.POST)
		if form.is_valid():
                        username = request.session['username']
                        user_id = User.get_user_by_username(username).id
                        User.create_new_tool(user_id, request.POST['toolname'],request.POST['description'],request.POST['tooltype'])
                    
                        return HttpResponseRedirect('/user/tools/')
	
	form = CreateTool()			
	html = render(request, 'add_tool.html', {'form':form})
	return HttpResponse(html)


def tool_editor(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
	username = request.session['username']
	user_id = User.get_user_by_username(username).id
	fields = {'Tool': User.get_all_user_tools(user_id)}
                  	
	html = render(request, 'tool_editor.html', fields)
	return HttpResponse(html)
