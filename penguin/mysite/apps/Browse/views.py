from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..Users.models import User
from ..Tools.models import Tool
from .models import BorrowTransaction

# Create your views here.


def browse_tools(request):
	if 'username' not in request.session:
		return HttpResponseRedirect('/')
	if(request.method == 'POST'):

		for key in request.POST:
			if request.POST[key] == 'Borrow!':
				request.session['currently_borrowing'] = key

		return HttpResponseRedirect('/browse/borrow/')

	area_code = request.session['area_code']
	tools =  Tool.get_tool_by_area_code(area_code)
	for tool in tools:
		tool.is_available = Tool.is_tool_available(tool.id)
	context = { 'tool_list': tools,
		'user_ac': area_code,
	}
	html = render(request, 'browse.html', context)
	return HttpResponse(html)


def borrow_tool(request):
	if 'username' not in request.session or 'currently_borrowing' not in request.session:
		return HttpResponseRedirect('/')
	currently_editing = Tool.get_tool(request.session['currently_borrowing'])

	if(request.method == 'POST'):	
		del request.session['currently_borrowing']
		Tool.set_tool_unavailable(currently_editing.id, int(request.POST['days']))
		user = User.get_user(request.session['id'])
		BorrowTransaction.create_new_borrow_transaction(user, currently_editing)
		return HttpResponseRedirect('/browse')

	html = render(request, 'borrow.html', {'tool': currently_editing, 'tool_pickup_arrangements': currently_editing.tool_pickup_arrangements})
	return HttpResponse(html)



