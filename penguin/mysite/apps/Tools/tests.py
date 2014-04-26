from django.test import TestCase
import unittest

# For testing the Tool API Routes
from .api_routes import *
from django.test.client import RequestFactory

# For testing the Tool model
from .models import Tool
from ..Users.models import User		# Linked in database
import datetime
from django.utils import timezone



""" Unit Test the Tools model. 

UPDATE: no longer need to set pk's manually, apparently you *can* store
objects for later use. I shouldn't be relying on constant pk's anyway.
"""                
class ToolTestCase(TestCase):

	def setUp(self):
		# Set up sample User
		self.john = User(
			username = 'John', 
			hashed_password = 'password',	#not actually hashed
			salt = 'NaCl',
			zip_code = '00413', 
			email = 'ectoBiologist@skaia.net', 
			phone_number = '1234567890', 
			default_pickup_arrangements = 'Drop in nearest mailbox.',
			)
		self.john.save()
		
		# Set up sample Tool
		today = timezone.now()
		self.sledge = Tool(
			name = "sledgehammer", 
			owner = self.john, 
			description = "A sturdy sledgehammer.", 
			tool_type = "hammer",
			tool_pickup_arrangements =
				"If you can lift it, you can have it.",
			available_date = today,
			)
		self.sledge.save()
	
	def test_create_new_tool(self):
		john = self.john
		zillyhoo0 = Tool.create_new_tool(
			toolname = "Warhammer of Zillyhoo",
			toolownerID = john.id,
			tooldescription = "Its majesty makes you weep.",
			tooltype = "hammer", 
			toolshed = False, 
			pickup_info = "Some time travel required.",
			)
		
		# slight hack here: the create_new_tool() method doesn't allow 
		# you to manually set the private key, so I'm just trusting 
		# that the name is unique enough.
		zillyhoo = Tool.objects.get(name="Warhammer of Zillyhoo")
		self.assertEqual(zillyhoo.name, "Warhammer of Zillyhoo")
		self.assertEqual(zillyhoo.owner, john)
		self.assertEqual(zillyhoo.description, 
			"Its majesty makes you weep.")
		self.assertEqual(zillyhoo.tool_type, "hammer")
		self.assertEqual(zillyhoo.tool_pickup_arrangements, 
			"Some time travel required.")
		self.assertEqual(zillyhoo0, zillyhoo)
	
	def test_update_tool(self):
		#update the tool
		john = self.john
		sledge = self.sledge
		Tool.update_tool(
			toolID = sledge.id, 
			toolname = "broken sledgehammer", 
			tooldescription = "Basically a stick.",
			tooltype = "1/2 hammer",
			shed = False,
			pickup_info = "Take it off my lawn.",
			tool_available = True,
			)
		
		#re-get the tool after updating it
		broken_sledge = Tool.objects.get(pk=sledge.pk)
		
		#check that the update did what was expected
		self.assertEqual(broken_sledge.name, "broken sledgehammer")
		self.assertEqual(broken_sledge.owner, john)
		self.assertEqual(broken_sledge.description, 
			"Basically a stick.")
		self.assertEqual(broken_sledge.tool_type, "1/2 hammer")
		#self.assertEqual(broken_sledge.shed, "12345")
		self.assertEqual(broken_sledge.in_community_shed, False)
		self.assertEqual(broken_sledge.tool_pickup_arrangements, 
			"Take it off my lawn.")
	
	def test_delete_tool(self):
		sledge = self.sledge
		self.assertIn(sledge, Tool.objects.all())
		Tool.delete_tool(sledge.id)
		self.assertNotIn(sledge, Tool.objects.all())
	
	def test_get_tool(self):
		sledge = self.sledge
		sledge2 = Tool.get_tool(sledge.id)
		self.assertEqual(sledge, sledge2)
	
	def test_get_tool_id(self):
		sledge = self.sledge
		num = Tool.get_tool_id(sledge)
		self.assertEqual(num, sledge.id) 	#should never fail
	
	def test_set_tool_unavailable(self):
		#in our test database, it should be available initially...
		sledge = self.sledge
		self.assertTrue(sledge.available_date < timezone.now())
		
		#but then let's mark it as away for a week.
		Tool.set_tool_unavailable(
			sledge.id, 
			timezone.now() + datetime.timedelta(days=7),
			)
		sledge = Tool.objects.get(pk=sledge.pk)
		self.assertFalse(sledge.available_date < timezone.now())
	
	def test_is_tool_available(self):
		# Fresh tool should be available from the start
		sledge = self.sledge
		self.assertTrue(Tool.is_tool_available(sledge.id))
		
		# Flag the tool as checked out like this
		sledge.is_available = False
		sledge.save()
		self.assertFalse(Tool.is_tool_available(sledge.id))
	
	""" def test_is_tool_available_future_date(self):
		
		This functionality has changed, the date is an "expected" date,
		not a hard deadline. It's possible for us to pass a date but
		still not have the tool back yet.
		
		#if we move the date, it should no longer be available
		sledge = self.sledge
		sledge.available_date = timezone.now() + \
			datetime.timedelta(days=1)
		sledge.save()
		self.assertFalse(Tool.is_tool_available(sledge.id))
	"""
	
	@unittest.expectedFailure
	def test_is_tool_available_deleted(self):
		#if a tool is deleted, it should *definitely* not be available.
		id = self.sledge.id
		self.sledge.delete()
		self.assertFalse(Tool.is_tool_available(id))
"""
	def test_get_tool_owner(self):
		sledge = Tool.objects.get(pk=23)
		parrot = User.objects.get(pk=42)
		self.assertEqual(Tool.get_tool_owner(sledge.id), parrot)

	def test_get_tool_by_area_code(self):
		localTools = Tool.get_tool_by_area_code("03545")
		#the Sledgehammer (pk = 23) should exist in this area code.
		self.assertTrue(localTools.filter(pk=23).exists())
"""

""" Test the API Routes in this app """
class ToolApiTestCase(TestCase):
	
	def setUp(self):
		# Set up a Request Factory
		self.factory = RequestFactory()
		
		# Set up a User
		self.john = User(
			username='John', 
			hashed_password = 'password', 
			salt = 'NaCl',
			zip_code = '00413', 
			email = 'ectoBiologist@skaia.net', 
			phone_number = '1234567890', 
			default_pickup_arrangements = 
				'Drop in nearest mailbox.',
			)
		self.john.save()
		
		# Set up a Tool
		today = timezone.now()
		self.sledge = Tool(	
			name = "sledgehammer", 
			owner = self.john, 
			description = "A sturdy sledgehammer.", 
			tool_type = "hammer",
			tool_pickup_arrangements =
				"If you can lift it, you can have it.",
			available_date = today,
			)
		self.sledge.save()
		
		# JSON Data for a new tool
		self.needles_info = {
			"name" : "Knitting Needles",
			"description" : "for making plush eldrich monstrosities",
			"tool_type" : "needle",
			"in_community_shed" : "True",
			"tool_pickup_arrangements" : "Get it from the shed."
			}
			
		# Mock session, where applicable
		self.mock_session = \
		{
			"user" : \
			{
				"id" : self.john.id
			}
		}
		
	
	def test_getById(self):
		request = self.factory.get('/api/tool/')
		response = get_tool(request, self.sledge.id)
		
		# Did we get a clean response?
		self.assertEqual(response.status_code, 200)
		
		# Did we get the right data?
		# NOTE: Instead of the owner object, we'll be getting back
		# the owner's username, and instead of a date object, we'll
		# be getting a datetime in milliseconds.
		response_data = json.loads(response.content.decode("utf-8"))
		self.assertEqual(response_data["name"], self.sledge.name)
		self.assertEqual(response_data["owner"], 
			self.sledge.owner.username,
			)
		self.assertEqual(response_data["description"], 
			self.sledge.description,
			)
		self.assertEqual(response_data["tool_type"], 
			self.sledge.tool_type,
			)
		self.assertEqual(response_data["tool_pickup_arrangements"], 
			self.sledge.tool_pickup_arrangements,
			)
		self.assertEqual(response_data["available_date"], 
			dt_to_milliseconds(self.sledge.available_date),
			)
	
	def test_createNewTool(self):
		request = self.factory.post(
			path = '/api/tool/', 
			data = json.dumps(self.needles_info), 
			content_type = "application/json"
			)
		request.session = self.mock_session
		
		response = update(request)
		response_data = json.loads(response.content.decode("utf-8"))
		
		# No way to know the new ID, but here's some stuff it isn't!
		self.assertIsNotNone(response_data["id"])
		self.assertNotEqual(response_data["id"], 0)
		
		# Also no way to know the exact time of creation, but all that
		# we care about right now is that it's in the past.
		self.assertTrue(response_data["available_date"] - 
			dt_to_milliseconds(timezone.now()) < 0 )
		
		# And now the rest of the validation.
		self.assertEqual(response_data["name"], 
			self.needles_info["name"])
		self.assertEqual(response_data["owner"], 
			self.john.username)
		self.assertEqual(response_data["description"], 
			self.needles_info["description"])
		self.assertEqual(response_data["tool_type"], 
			self.needles_info["tool_type"])
		self.assertEqual(response_data["in_community_shed"], 
			self.needles_info["in_community_shed"])
		self.assertEqual(response_data["tool_pickup_arrangements"], 
			self.needles_info["tool_pickup_arrangements"])
		self.assertTrue(response_data["tool_available"])
		
		
	def test_updateTool(self):
		request = self.factory.put('/api/tool')
		return
		
	def test_deleteTool(self):
		request = self.factory.delete('/api/tool')
		return
		
	def test_getLocalTools(self):
		request = self.factory.get('/api/tools/area')
		return
		
	def test_getPersonalTools(self):
		request = self.factory.get('/api/tools')
		return

