from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Tool
from ..Users.models import User		# Linked in database

""" Test the creation and usage of tools. """                
class ToolTestCase(TestCase):

	def setUp(self):
		# Tools require an Owner, so let's add a user:
		john = User(pk=42, 
					username='John', 
					password = 'password', 
					area_code = '00413', 
					email = 'ectoBiologist@skaia.net', 
					phone_number = '1234567890', 
					default_pickup_arrangements = 
						'Drop in nearest pipe.',
					)
		john.save()
		
		# Remember you can always identify a tool by its private key,
		# though.
		today = timezone.now()
		sledge = Tool(	
			pk = 23, 
			name = "sledgehammer", 
			owner = john, 
			description = "A sturdy sledgehammer.", 
			tool_type = "hammer",
			tool_pickup_arrangements =
				"If you can lift it, you can have it.",
			available_date = today,
			)
		sledge.save()


	def test_create_new_tool(self):
		john = User.objects.get(pk=42)
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
		john = User.objects.get(pk=42)
		sledge = Tool.objects.get(name = "sledgehammer")
		Tool.update_tool(
			toolID = sledge.id, 
			toolname = "broken sledgehammer", 
			tooldescription = "Basically a stick.",
			tooltype = "1/2 hammer",
			shed = False,
			pickup_info = "Take it off my lawn.",
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
		
"""
	def test_delete_tool(self):
		Tool.objects.filter(pk=42)
		return
"""

"""
	def test_get_tool(self):
		sledge = Tool.get_tool(23)
		self.assertEqual(sledge.name, "sledgehammer")
		
	def test_set_tool_unavailable(self):
		#in our test database, it should be available initially...
		sledge = Tool.objects.get(pk=23)
		self.assertTrue(sledge.available_date < timezone.now())
		
		#but then let's mark it as away for a week.
		Tool.set_tool_unavailable(sledge.id, 7)
		sledge = Tool.objects.get(pk=sledge.pk)
		self.assertFalse(sledge.available_date < timezone.now())
		
				
	def test_is_tool_available(self):
		#again, the fresh tool should be available from the start
		sledge = Tool.objects.get(pk=23)
		self.assertTrue(Tool.is_tool_available(sledge.id))
		
		#but if we move the date, it should break.
		sledge.available_date = timezone.now() + datetime.timedelta(days=1)
		sledge.save()
		self.assertFalse(Tool.is_tool_available(sledge.id))
		
	def test_get_tool_owner(self):
		sledge = Tool.objects.get(pk=23)
		parrot = User.objects.get(pk=42)
		self.assertEqual(Tool.get_tool_owner(sledge.id), parrot)

	def test_get_tool_by_area_code(self):
		localTools = Tool.get_tool_by_area_code("03545")
		#the Sledgehammer (pk = 23) should exist in this area code.
		self.assertTrue(localTools.filter(pk=23).exists())
"""
