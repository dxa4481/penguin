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
	tools = User.get_all_user_tools(request.session['id'])
	for tool in tools:
                tool.is_available = Tool.is_tool_available(tool.id)
	context = { 'Tools': tools, 'username': username,}

	if(request.method == 'POST'):
		form = CreateTool(request.POST)
		for key in request.POST:
			if request.POST[key] == 'Edit!':	
				request.session['currently_editing'] = key
		return HttpResponseRedirect('/user/tools/edit/')


	return render(request, 'user_tools.html', context)

	#return HttpResponse("This is a test of the User Tools page. Quack.")






def new_tool(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		form = CreateTool(request.POST)
		if form.is_valid():
			print(request.POST)
			if request.POST['shed'] != '1':
				shed = "community"
			else:
				shed = request.session['username']
			User.create_new_tool(request.session['id'], request.POST['toolname'],request.POST['description'],request.POST['tooltype'], shed)
                    
			return HttpResponseRedirect('/user/tools/')
	
	form = CreateTool()			
	html = render(request, 'add_tool.html', {'form':form})
	return HttpResponse(html)


def tool_editor(request):
	if 'username' not in request.session or 'currently_editing' not in request.session:
		return HttpResponseRedirect('/')
	currently_editing = Tool.get_tool(request.session['currently_editing'])
	del request.session['currently_editing']
	
	html = render(request, 'tool_editor.html', {})

	return HttpResponse(html)
