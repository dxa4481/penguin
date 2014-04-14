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
		return_tool = { "id" : tool.id,
				"name" : tool.name, 
				"owner" : tool.owner.username,
				"available_date" : dt_to_milliseconds(tool.available_date),
				"description" : tool.description,
				"tool_type" : tool.tool_type,
				"community_shed" : tool.in_community_shed,
				"tool_pickup_arrangements": tool.tool_pickup_arrangements}
		return HttpResponse(json.dumps(return_tool), content_type="application/json")

@csrf_exempt
def create(request):
	if request.method == "GET":
		new_tool = create_new_tool(tool.name, tool.owner, tool.description, tool.tool_type, tool.shed, tool.tool_pickup_arrangements)
		