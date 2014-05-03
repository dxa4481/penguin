from django.db import models
import datetime
from django.utils import timezone
from ..Users.models import User


class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(User)
	available_date = models.DateTimeField()
	is_available = models.BooleanField(default=True)
	description = models.CharField(max_length=250)
	tool_type = models.CharField(max_length=30)
	in_community_shed = models.BooleanField(default=False)
	tool_pickup_arrangements = models.CharField(max_length=250)


	
	def __str__(self):
		return (self.name)

	""" Constructor to add a new tool
	STATIC METHOD
	:param toolname: name of tool
	:param toolownerID: ID of owner of the tool
	:param tooldescription: description of tool
	:param tooltype: type of tool
	:param shed: true if tool is in community shed, false otherwise
	:param pickup_info: the tool's pickup arrangements
	:return The tool that was just added
	"""
	@staticmethod
	def create_new_tool(toolname, toolownerID, tooldescription, tooltype, toolshed, pickup_info):
		t = Tool(name=toolname, owner=User.get_user(toolownerID), description=tooldescription, tool_type=tooltype, in_community_shed=toolshed, tool_pickup_arrangements=pickup_info)
		t.available_date = timezone.now() - datetime.timedelta(days=5)
		t.save()
		return t
		
	""" Updates a tool's information
	STATIC METHOD
	:param toolID: tool's ID
	:param toolname: name of tool
	:param tooldescription: description of tool
	:param tooltype: type of tool
	:param toolshed: true if tool is in community shed, false otherwise
	:param pickup_info: the tool's pickup arrangements
	"""
	@staticmethod
	def update_tool(toolID, toolname, tooldescription, tooltype, shed, pickup_info, tool_available):
		t = Tool.get_tool(toolID)
		t.name = toolname
		t.description = tooldescription
		t.tool_type = tooltype
		t.in_community_shed = shed
		t.tool_pickup_arrangements = pickup_info
		t.is_available = tool_available
		t.save()
	
	""" Deletes the given tool
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def delete_tool(toolID):
		t = Tool.get_tool(toolID)
		t.delete()

	""" Returns tool based on ID
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def get_tool(toolID):
		tool_list = Tool.objects.filter(pk=toolID)
		if(len(tool_list) == 0):
			return False
		else:
			return tool_list[0]
		
		
	""" Return tool's ID
	"""
	def get_tool_id(self):
		return self.id
	
	""" Sets a tool as unavailable for a given number of days
	STATIC METHOD
	:param toolID: tool's ID
	:param end_date: the date that the tool will be available once more
	"""
	@staticmethod
	def set_tool_unavailable(toolID, end_date):
		t = Tool.get_tool(toolID)
		t.available_date = end_date
		t.is_available = False
		t.save()
		return t

	
	"""Sets a tool as available
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def set_tool_available(toolID):
		t = Tool.get_tool(toolID)
		t.available_date = timezone.now() - datetime.timedelta(seconds=1)
		t.is_available = True
		t.save()
	
	""" Checks if a tool is available now
	STATIC METHOD
	:param toolID: tool's ID
	:return true if the rent date is less than today, false otherwise
	"""
	@staticmethod
	def is_tool_available(toolID):
		t = Tool.get_tool(toolID)
		return t.is_available


	""" Get tool's owner's id
	STATIC METHOD
	:param toolID: tool's ID
	:return owner's id
	"""
	@staticmethod
	def get_tool_owner(toolID):
		t = Tool.get_tool(toolID)
		return t.owner
		
	""" Get the tool list in a certain zip code
	:param ac: zip code to search in
	:return list of tools in that zip code
	"""
	@staticmethod
	def get_tool_by_zip_code(zip_c):
		return Tool.objects.filter(owner__zip_code__exact=zip_c)

	"""Get all tools belonging to an owner
	STATIC METHOD
	:param ownerID: owner's ID
	:returns list of tools belonging to that owner
	"""
	@staticmethod
	def get_tool_by_owner(ownerID):
		return Tool.objects.filter(owner__id__exact=ownerID)
