from django.db import models

from ..Users.models import User

class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	#owner = models.ForeignKey('User')
	is_available = models.BooleanField(default=True)
	description = models.CharField(max_length=250)
	tool_type = models.CharField(max_length=30)
	
	def __str__(self):
		return (str(self.id) + ':' + self.name)

	""" Constructor to add a new tool
	STATIC METHOD
    :param n: name of tool
    :param d: description of tool
    :param t: type of tool
    :return The tool that was just added
    """
	@staticmethod
	def create_new_tool(n, d, tt):
		t = Tool(name=n, description=d, tool_type=tt)
		t.save()
		return t
		
	""" Deletes the given tool
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def delete_tool(toolID):
		t = Tool.get_tool(toolID)
		t.delete()

	""" Returns tool based on ID
	"""
	@staticmethod
	def get_tool(toolID):
		return Tool.objects.get(pk=toolID)
		
		
	""" Return tool's ID
	"""
	def get_tool_id(self):
		return self.id

	"""Sets a tool as unavailable
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def set_tool_unavailable(toolID):
		t = Tool.get_tool(toolID)
		t.is_available = False
		t.save()

	""" Sets a tool as available
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def set_tool_available(toolID):
		t = Tool.get_tool(toolID)
		t.is_available = True
		t.save()

	"""Checks if tool is available
	STATIC METHOD
	:param toolID: tool's ID
	:return true if available, false otherwise
	"""
	@staticmethod
	def is_tool_available(toolID):
		t = Tool.get_tool(toolID)
		return t.is_available

	#INCOMPLETE
	""" Get tool's owner's id
	STATIC METHOD
	:param toolID: tool's ID
	:return owner's id
	"""
	@staticmethod
	def get_tool_owner(toolID):
		return OwnTool.get(tool=toolID).owner


class OwnTool(models.Model):
	id = models.AutoField(primary_key=True)
	owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	tool = models.ForeignKey(Tool)

	def __str__(self):
		return (str(self.id) + ' o:' + str(self.owner) + ' t:' + str(self.tool))
	
	
	"""Create a new tool ownership
	STATIC METHOD
	:param o: owner object
	:param t: tool object
	"""
	@staticmethod
	def create_new_tool_ownership(o, t):
		own = OwnTool(owner=o,
		tool=t)
		own.save()

	""" Remove a tool ownership
	STATIC METHOD
	:param otID: OwnTool relation's ID
	"""
	@staticmethod
	def remove_tool_ownership(otID):
		ot = OwnTool.get_tool_ownership(otID)
		ot.delete()

	""" Return a tool ownership by id
	STATIC METHOD
	:param otID: OwnTool relation's ID
	"""
	@staticmethod
	def get_tool_ownership(otID):
		return OwnTool.objects.get(pk=otID)

	"""Get a tool ownership's id
	:return id of tool ownership
	"""
	def get_tool_ownership_id(self):
		return self.id

