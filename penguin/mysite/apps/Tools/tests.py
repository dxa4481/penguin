from django.test import TestCase
import datetime
from django.utils import timezone

from .models import *

""" Test the creation and usage of users. """
class UserTestCase(TestCase):
	def setUp(self):
		# Assume all usernames are unique, use them for lookup.
		parrot = User(pk = 42, username='Parrot', password = 'password', area_code = '03545', email = 'polly@python.org', phone_number = '1234567890', default_pickup_arrangements = 'Pining for the fjords.')
		parrot.save()
		af_swallow = User(pk = 2, username = 'African_Swallow', password = 'password', area_code = '03545', email = 'swallow@python.org', phone_number = '1234567890', default_pickup_arrangements = 'Incapable of lifting a coconut.')
		af_swallow.save()
		eu_swallow = User(pk = 3, username = 'European_Swallow', password = 'password', area_code = '03545', email = 'swallow@python.org', phone_number = '1234567890', default_pickup_arrangements = 'Capable of lifting a coconut.')
		eu_swallow.save()

	def test_create_new_user(self):
		penguin0 = User.create_new_user('Penguin', 'password', '03545', 'penguin@python.org', '5555551234', 'It\'s on the telly.')
		penguin = User.objects.get(username='Penguin')

		self.assertEqual(penguin.username, 'Penguin')
		self.assertEqual(penguin.password, 'password')
		self.assertEqual(penguin.area_code, '03545')
		self.assertEqual(penguin.email, 'penguin@python.org')
		self.assertEqual(penguin.phone_number, '5555551234')
		self.assertEqual(penguin.default_pickup_arrangements, 'It\'s on the telly.')
		self.assertEqual(penguin0, penguin)

	def test_update_user(self):
		# NOTE: have to make changes BEFORE query, because query returns value not reference.
		User.update_user("African_Swallow", "18005555555", "12345", "afswallow@python.edu", "Tie it to a length of string")
		af_swallow = User.objects.get(username = "African_Swallow")
		self.assertEqual(af_swallow.username, 'African_Swallow')
		self.assertEqual(af_swallow.password, 'password')
		self.assertEqual(af_swallow.area_code, '12345')
		self.assertEqual(af_swallow.email, 'afswallow@python.edu')
		self.assertEqual(af_swallow.phone_number, '18005555555')
		self.assertEqual(af_swallow.default_pickup_arrangements, "Tie it to a length of string")

	def test_get_user(self):
		guy = User.get_user(42)
		self.assertEqual(guy.id, 42)
		self.assertEqual(guy.username, "Parrot")

	def test_get_user_by_username(self):
		guy = User.get_user_by_username("Parrot")
		self.assertEqual(guy.id, 42)
		self.assertEqual(guy.username, "Parrot")

#	def test_create_new_tool(self):
#	def test_get_all_user_tools(self):

""" Test the creation and usage of tools. """                
class ToolTestCase(TestCase):

	def setUp(self):
		# Tools require an Owner, so let's add a user:
		parrot = User(pk=42, username='Parrot', password = 'password', area_code = '03545', email = 'polly@python.org', phone_number = '1234567890', default_pickup_arrangements = 'Pining for the fjords.')
		parrot.save()
		
		# Remember you can always identify a tool by its private key though.
		today = timezone.now()
		sledge = Tool(pk=23, name="sledgehammer", owner=parrot, description="A sturdy sledgehammer.", tool_type="hammer", shed="03545", tool_pickup_arrangements="If you can lift it, you can have it.", available_date = today)
		sledge.save()

	def test_create_new_tool(self):
		parrot = User.objects.get(pk=42)
		zillyhoo0 = Tool.create_new_tool("Warhammer of Zillyhoo", parrot, "Its majesty makes you weep.", "hammer", "03545", "Some time travel required.")
		# slight hack here: the create_new_tool() method doesn't allow you
		# to manually set the private key, so I'm just trusting that the
		# name is unique enough.
		zillyhoo = Tool.objects.get(name="Warhammer of Zillyhoo")
		self.assertEqual(zillyhoo.name, "Warhammer of Zillyhoo")
		self.assertEqual(zillyhoo.owner, parrot)
		self.assertEqual(zillyhoo.description, "Its majesty makes you weep.")
		self.assertEqual(zillyhoo.tool_type, "hammer")
		self.assertEqual(zillyhoo.shed, "03545")
		self.assertEqual(zillyhoo.tool_pickup_arrangements, "Some time travel required.")
		self.assertEqual(zillyhoo0, zillyhoo)
	
	def test_update_tool(self):
		#update the tool
		parrot = User.objects.get(pk=42)
		sledge = Tool.objects.get(name = "sledgehammer")
		Tool.update_tool(sledge.pk, "broken sledgehammer", "Basically a stick.", "1/2 hammer", "12345", "Take it off my lawn.")
		
		#re-get the tool after updating it
		broken_sledge = Tool.objects.get(pk=sledge.pk)
		
		#check that the update did what was expected
		self.assertEqual(broken_sledge.name, "broken sledgehammer")
		self.assertEqual(broken_sledge.owner, parrot)
		self.assertEqual(broken_sledge.description, "Basically a stick.")
		self.assertEqual(broken_sledge.tool_type, "1/2 hammer")
		self.assertEqual(broken_sledge.shed, "12345")
		self.assertEqual(broken_sledge.tool_pickup_arrangements, "Take it off my lawn.")
		
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
	
	

#class BorrowTransactionTestCase(TestCase):

#	def test_create_new_borrow_transaction(self):
#	def test_get_borrow_transaction(self):
#	def test_get_borrower_borrow_transactions(self):
#	def test_is_current(self):
