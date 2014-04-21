from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import Tool
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt


@csrf_exempt
def update(request):
	if request.method == "PUT":
		put_data = json.loads(request.body.decode("utf-8"))
		tool_id = int(put_data["id"])
		Tool.update_tool(tool_id,
				put_data["name"],
				put_data["description"],
				put_data["tool_type"],
				put_data["in_community_shed"],
				put_data["tool_pickup_arrangements"])
		tool = Tool.get_tool(tool_id)
		return_tool = tool_to_json(tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")

	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		new_tool = Tool.create_new_tool(post_data["name"], 
				request.session["user"]["id"], 
				post_data["description"], 
				post_data["tool_type"], 
				post_data["in_community_shed"],
				post_data["tool_pickup_arrangements"])
		return_tool = tool_to_json(new_tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")

	
@csrf_exempt
def get_tool(request, tool_id):
	if request.method == "GET":
		tool_id = int(tool_id)
		tool = Tool.get_tool(tool_id)
		return_tool = tool_to_json(tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")
		
	"""
	^/api/tool/:id DELETE
	Known risks:
	  * Tool can be deleted by users other than the one who owns it.
	  * Tool can be deleted while it's checked out.
	"""
	if request.method == "DELETE":
		try:
			Tool.delete_tool(tool_id)
			returnmsg = { 'success': True }
		except:
			returnmsg = { 'success': False }
			 
		return HttpResponse(json.dumps(returnmsg), content_type="application/json")
"""
@csrf_exempt
def create(request):
	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		new_tool = Tool.create_new_tool(post_data.name, request.session["user"]["id"], 
				post_data.description, post_data.tool_type, post_data.community_shed, 
				post_data.tool_pickup_arrangements)
		return_tool = tool_to_json(tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")
"""
"""		return_tool = { "id" : new_tool.id,
				"name" : new_tool.name, 
				"owner" : new_tool.owner.username,
				"available_date" : dt_to_milliseconds(new_tool.available_date),
				"description" : new_tool.description,
				"tool_type" : new_tool.tool_type,
				"community_shed" : new_tool.in_community_shed,
				"tool_pickup_arrangements" : new_tool.tool_pickup_arrangements}
"""		
		#print(new_tool)
		

"""	if request.method == "GET":
		new_tool = create_new_tool(tool.name, tool.owner, tool.description, tool.tool_type, tool.shed, tool.tool_pickup_arrangements)
"""		

@csrf_exempt
def user_tools(request):
	"""
	^/api/tools/ GET
	Known risks:
	  * None
	"""
	#get user_id from the request object
	if request.method == "GET":
		user_id = request.session["user"]["id"]
		tool_list = Tool.get_tool_by_owner(user_id)
		return_list = []
		
		for tool in tool_list:
			return_list.append(tool_to_json(tool))
		
		return HttpResponse(json.dumps(return_list), content_type="application/json")
	
@csrf_exempt
def local_tools(request):
	"""
	^/api/tools/:ac GET
	Known risks:
	  * None
	"""
	#get zip code from the request object
	if request.method == "GET":
		zip_code = request.session["user"]["zip_code"]
		tool_list = Tool.get_tool_by_zip_code(zip_code)
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
			"in_community_shed" : tool.in_community_shed,
			"tool_pickup_arrangements": tool.tool_pickup_arrangements}
	return return_tool
