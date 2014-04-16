from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import Tool
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt


@csrf_exempt
def update(request):
	return 0
	#if request.method == "PUT"
		#put_data = json.loads(request.body.decode("utf-8"))
	
	
@csrf_exempt
def getTool(request, tool_id):
	tool_id = int(tool_id)
	print(tool_id)
	if request.method == "GET":
		tool = Tool.get_tool(tool_id)
		return_tool = tool_to_json(tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")
		
	if request.method == "DELETE":
		try:
			Tool.delete_tool(tool_id)
			returnmsg = { 'success': True }
		except:
			returnmsg = { 'success': False }
			 
		return HttpResponse(json.dumps(returnmsg), content_type="application/json")

@csrf_exempt
def create(request):
	if request.method == "GET":
		new_tool = create_new_tool(tool.name, tool.owner, tool.description, tool.tool_type, tool.shed, tool.tool_pickup_arrangements)
		

@csrf_exempt
def user_tools(request):
	#get user_id from the request object
	if request.method == "GET":
		user_id = request.session['user']['id']
		tool_list = Tool.get_tool_by_owner(user_id)
		return_list = []
		
	for tool in tool_list:
		return_list.append(tool_to_json(tool))
		
	return HttpResponse(json.dumps(return_list), content_type="application/json")
	
@csrf_exempt
def local_tools(request):
	#get area code from the request object
	if request.method == "GET":
		area_code = request.session['user']['area_code']
		tool_list = Tool.get_tool_by_area_code(area_code)
		return_list = []
		
		for tool in tool_list:
			return_list.append(tool_to_json(tool))
			
		return HttpResponse(json.dumps(return_list), content_type="application/json")
		
"""
Helper method: convert tool to JSON. We do this a lot in this file.
"""
def tool_to_json(tool):
	return_tool = { "id" : tool.id,
			"name" : tool.name, 
			"owner" : tool.owner.username,
			"available_date" : dt_to_milliseconds(tool.available_date),
			"description" : tool.description,
			"tool_type" : tool.tool_type,
			"community_shed" : tool.in_community_shed,
			"tool_pickup_arrangements": tool.tool_pickup_arrangements}
	return return_tool
