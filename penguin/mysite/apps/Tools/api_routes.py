from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import Tool
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt
from ..Users.models import User

@csrf_exempt
def update(request):
	"""
	edit a tool
	PUT
	url -> /api/tool

	possible errors:
	id not an int
	tool being borrowed -- cannot edit
	"""
	if request.method == "PUT":
		put_data = json.loads(request.body.decode("utf-8"))
		# user not logged in -- error 401
		try:
			request.session['user']
		except KeyError:
			error = {"error": "access denied, no user logged in"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=401)

		tool_id = int(put_data["id"])
		current_user = User.get_user(request.session['user']['id'])

		if current_user == False:
			error = {"error": "oops. something went wrong, try refreshing page"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=410)

		# tool does not exist -- error 410
		current_tool = Tool.get_tool(tool_id)
		if current_tool == False:
			error = {"error": "something went wrong, try refreshing"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=410)

		#Validate user is owner of tool, or admin
		if ((current_user.is_admin==True) or (Tool.get_tool(tool_id).owner==current_user)):

			# tool is currently being borrowed -- error 400
			current_tool = Tool.get_tool(tool_id)
			if not current_tool.is_available:
				error = {"error": "tool is being borrowed, cannot edit attributes"}
				return HttpResponse(json.dumps(error), content_type="application/json", status=400)

			# pickup arrangements field left blank -- revert to user's default pickup arrangements
			pickup_arrangement = current_user.default_pickup_arrangements
			if put_data["tool_pickup_arrangements"]:
				pickup_arrangement = put_data["tool_pickup_arrangements"]
	
			Tool.update_tool(tool_id,
					put_data["name"],
					put_data["description"],
					put_data["tool_type"],
					put_data["in_community_shed"],
					pickup_arrangement, 
					put_data["tool_available"])
			tool = Tool.get_tool(tool_id)
			return_tool = tool_to_json(tool)
			return HttpResponse(json.dumps(return_tool), content_type="application/json")
		else:
			error = {"error": "You are not authorized to edit this tool."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=401)

	#Create a tool
	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		# make sure user is logged in first -- error 401
		try:
			current_user = User.get_user_by_username(request.session["user"]["username"])
		except KeyError:
			error = {"error": "access denied, you are currently not logged in"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=401)
		
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
#		current_user = User.get_user_by_username(request.session["user"]["username"])
		pickup_arrangements = current_user.default_pickup_arrangements
		if post_data["tool_pickup_arrangements"]:
			pickup_arrangements = post_data["tool_pickup_arrangements"]

		new_tool = Tool.create_new_tool(post_data["name"], 
				request.session["user"]["id"], 
				post_data["description"], 
				post_data["tool_type"], 
				post_data["in_community_shed"],
				pickup_arrangements,
				post_data["tool_available"])
		return_tool = tool_to_json(new_tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")

"""
get tool
GET

possible errors:
tool does not exist
tool id is not an int
"""
@csrf_exempt
def get_tool(request, tool_id):
	if request.method == "GET":
		# no user logged in -- error 401
		try:
			request.session['user']['id']
		except KeyError:
			error = {"error": "access denied, no user logged in"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=401)
		# tool id is not an int -- error 400
		try:
			tool_id = int(tool_id)
		except ValueError:
			error = {"error": "tool id not an int"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		tool = Tool.get_tool(tool_id)
		
		# tool does not exist -- error 410
		if tool == False:
			error = {"error": "tool does not exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=410)

		return_tool = tool_to_json(tool)
		return HttpResponse(json.dumps(return_tool), content_type="application/json")
		
	"""
	^/api/tool/:id DELETE
	Known risks:
	  * Tool can be deleted by users other than the one who owns it.
	  * Tool can be deleted while it's checked out.
	"""
	if request.method == "DELETE":
		# no user logged in -- error 401
		try:
			request.session['user']
		except KeyError:
			error = {"error": "access denied, no user logged in"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# tool id not an int -- error 400
		try:
			int(tool_id)
		except ValueError:
			error = {"error": "tool id not an int"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# tool does not exist -- error 400
		current_tool = Tool.get_tool(tool_id)
		if current_tool == False:
			error = {"error": "something went wrong, try refreshing"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=410)

		#Validate user is owner of tool, or admin
		current_user = User.get_user_by_username(request.session['user']['username'])
		if current_user == False:
			error = {"error": "user doesn't exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=410)
		if ((current_user.is_admin==True) or (current_tool.owner==current_user)):
			# tool is being borrowed -- error 400
			if not current_tool.is_available:
				error = {"error": "tool is currently being borrowed, cannot delete"}
				return HttpResponse(json.dumps(error), content_type="application/json", status=400)
			try:
				Tool.delete_tool(tool_id)
				returnmsg = { 'success': True }
			except:
				returnmsg = { 'success': False }
				 
			return HttpResponse(json.dumps(returnmsg), content_type="application/json")
		else:
			error = {"error": "You are not authorized to edit this tool."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=401)

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
		current_user = User.get_user(user_id)
		if current_user == False:
			error = {"error": "user doesn't exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=410)
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
