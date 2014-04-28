from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import Tool
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt
from ..Users.models import User

def validate_fields(fields):
	for key in fields:
		if key == "tool_pickup_arrangements":
			pass
		elif not fields[key]:
			return False
	return True


@csrf_exempt
def update(request):
	if request.method == "PUT":
		put_data = json.loads(request.body.decode("utf-8"))
		tool_id = int(put_data["id"])

		if not validate_fields(put_data):
			error = {"error": "One or more fields were left blank, make sure all fields are filled in before submitting."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# pickup arrangements field left blank -- revert to user's default pickup arrangements
		current_user = User.get_user_by_username(request.session['user']['username'])
		pickup_arrangement = current_user.default_pickup_arrangements
		if put_data["tool_pickup_arrangements"]:
			pickup_arrangement = put_data["tool_pickup_arrangements"]

		# convert str representing bool to actual bool
		community_shed = False
		if put_data["in_community_shed"] == "True":
			community_shed = True

		# convert str representing bool to actual bool
		tool_available = True
		if put_data["tool_available"] == "False":
			tool_available = False

		Tool.update_tool(tool_id,
				put_data["name"],
				put_data["description"],
				put_data["tool_type"],
				community_shed,
				pickup_arrangement, 
				tool_available)
		tool = Tool.get_tool(tool_id)
		return_tool = tool_to_json(tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")

	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		
		shed = False
		if post_data["in_community_shed"] == "True":
			shed = True
		
		# tool name field left empty -- error 400
		if not post_data["name"]:
			error = {"error": "Tool name field left empty.  Please enter a tool name; this field cannot be left empty"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# tool description left empty -- error 400
		if not post_data["description"]:
			error = {"error": "Tool Description field left empty.  Please enter the tool's description; this field cannot be left empty"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# tool type field left empty -- error 400
		if not post_data["tool_type"]:
			error = {"error": "Tool Type field left empty.  Please enter the tool's type;  this field cannot be left empty."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# tool pickup arrangements left empty -- use user's default pickup arrangements
		current_user = User.get_user_by_username(request.session["user"]["username"])
		pickup_arrangements = current_user.default_pickup_arrangements
		if post_data["tool_pickup_arrangements"]:
			pickup_arrangements = post_data["tool_pickup_arrangements"]

		new_tool = Tool.create_new_tool(post_data["name"], 
				request.session["user"]["id"], 
				post_data["description"], 
				post_data["tool_type"], 
				shed,
				pickup_arrangements)
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
			"tool_pickup_arrangements": tool.tool_pickup_arrangements,
			"tool_available": tool.is_available}
	return return_tool
