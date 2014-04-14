from django.db import models
import datetime
from django.utils import timezone
from ..Users.models import User


class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	owner = models.ForeignKey(User)
	available_date = models.DateTimeField()
	#is_available = models.BooleanField(default=True)
	description = models.CharField(max_length=250)
	tool_type = models.CharField(max_length=30)
	#shed = models.CharField(max_length=30)
	in_community_shed = models.BooleanField(default=False)
	tool_pickup_arrangements = models.CharField(max_length=250)


	
	def __str__(self):
		return (self.name)

	""" Constructor to add a new tool
	STATIC METHOD
	:param toolname: name of tool
	:param toolowner: owner of the tool
	:param tooldescription: description of tool
	:param tooltype: type of tool
	:param toolshed: true if tool is in community shed, false otherwise
	:param pickup_info: the tool's pickup arrangements
	:return The tool that was just added
	"""
	@staticmethod
	def create_new_tool(toolname, toolowner, tooldescription, tooltype, toolshed, pickup_info):
		t = Tool(name=toolname, owner=toolowner, description=tooldescription, tool_type=tooltype, in_community_shed=toolshed, tool_pickup_arrangements=pickup_info)
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
	def update_tool(toolID, toolname, tooldescription, tooltype, shed, pickup_info):
		t = Tool.get_tool(toolID)
		t.name = toolname
		t.description = tooldescription
		t.tool_type = tooltype
		t.shed = shed
		t.tool_pickup_arrangements = pickup_info
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
		return Tool.objects.get(pk=toolID)
		
		
	""" Return tool's ID
	"""
	def get_tool_id(self):
		return self.id
	
	""" Sets a tool as unavailable for a given number of days
	STATIC METHOD
	:param toolID: tool's ID
	:param numDays: number of days unavailable
	"""
	@staticmethod
	def set_tool_unavailable(toolID, numDays):
		t = Tool.get_tool(toolID)
		t.available_date = timezone.now() + datetime.timedelta(days=numDays)
		t.save()

	""" Checks if a tool is available now
	STATIC METHOD
	:param toolID: tool's ID
	:return true if the rent date is less than today, false otherwise
	"""
	@staticmethod
	def is_tool_available(toolID):
		t = Tool.get_tool(toolID)
		if (t.available_date < timezone.now()):
			return True
		else:
			return False


	""" Get tool's owner's id
	STATIC METHOD
	:param toolID: tool's ID
	:return owner's id
	"""
	@staticmethod
	def get_tool_owner(toolID):
		t = Tool.get_tool(toolID)
		return t.owner
		
	""" Get the tool list in a certain area code
	:param ac: area code to search in
	:return list of tools in that area
	"""
	@staticmethod
	def get_tool_by_area_code(ac):
		return Tool.objects.filter(owner__area_code__exact=ac)

	"""Get all tools belonging to an owner
	STATIC METHOD
	:param ownerID: owner's ID
	:returns list of tools belonging to that owner
	"""
	@staticmethod
	def get_tool_by_owner(ownerID):
		return Tool.objects.filter(owner__id__exact=ownerID)