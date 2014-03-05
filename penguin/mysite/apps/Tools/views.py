from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

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

