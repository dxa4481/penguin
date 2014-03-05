from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# from models import Tool

# Display a list of tools
def user_tools(request):
	
	context = {'tool_list': ['hammer','chisel','toothbrush'] }
	return render(request, 'user_tools.html', context)
	#return HttpResponse("This is a test of the User Tools page. Quack.")

