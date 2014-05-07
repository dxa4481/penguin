#For unit testing
import unittest
from django.test import TestCase
import datetime
from django.utils import timezone

#For model testing
from .models import User
from ..Tools.models import Tool		# Linked in database

#For api testing
from django.test.client import RequestFactory
import json
from . import api_routes as api

""" Test the creation and usage of users. 
	Warning: these tests have not been updated in a while and are very
	out of date.
"""
class UserTestCase(TestCase):
	def setUp(self):
		# Assume all usernames are unique, use them for lookup.
		parrot = User(
			pk = 42, 
			username='Parrot', 
			hashed_password = 'password', 
			salt = "NaCl",
			zip_code = '03545', 
			email = 'polly@python.org', 
			phone_number = '1234567890', 
			default_pickup_arrangements = 'Pining for the fjords.'
			)
		parrot.save()
		af_swallow = User(
			pk = 2, 
			username = 'African_Swallow', 
			hashed_password = 'password', 
			salt = "NaCl",
			zip_code = '03545', 
			email = 'swallow@python.org', 
			phone_number = '1234567890', 
			default_pickup_arrangements = 
				'Incapable of lifting a coconut.',
			)
		af_swallow.save()
		eu_swallow = User(
			pk = 3, 
			username = 'European_Swallow', 
			hashed_password = 'password', 
			salt = "NaCl",
			zip_code = '03545', 
			email = 'swallow@python.org', 
			phone_number = '1234567890', 
			default_pickup_arrangements = 
				'Capable of lifting a coconut.',
			)
		eu_swallow.save()

	def test_create_new_user(self):
		penguin0 = User.create_new_user('Penguin', 'password', '03545', 'penguin@python.org', '5555551234', 'It\'s on the telly.')
		penguin = User.objects.get(username='Penguin')

		self.assertEqual(penguin.username, 'Penguin')
		#self.assertEqual(penguin.password, 'password') #can't compare this
		self.assertEqual(penguin.zip_code, '03545')
		self.assertEqual(penguin.email, 'penguin@python.org')
		self.assertEqual(penguin.phone_number, '5555551234')
		self.assertEqual(penguin.default_pickup_arrangements, 'It\'s on the telly.')
		self.assertEqual(penguin0, penguin)

	def test_update_user(self):
		# NOTE: have to make changes BEFORE query, because query returns value not reference.
		User.update_user("African_Swallow", "18005555555", "12345", "afswallow@python.edu", "Tie it to a length of string")
		af_swallow = User.objects.get(username = "African_Swallow")
		self.assertEqual(af_swallow.username, 'African_Swallow')
		#self.assertEqual(af_swallow.password, 'password') #we can't compare this
		self.assertEqual(af_swallow.zip_code, '12345')
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

	""" Deprecated - the User model is no longer in charge of 
		instantiating new Tools.
	"""
	@unittest.skip
	def test_create_new_tool(self):
		parrot = User.objects.get(username="Parrot")
		User.create_new_tool(parrot.id, "Coconut Threader", "For tying a length of thread between two coconuts", "needle", "parrot", "Stop by anytime.")
		coco = Tool.objects.get(name="Coconut Threader")
		self.assertEqual(coco.owner, parrot)
		self.assertEqual(coco.name, "Coconut Threader")
		self.assertEqual(coco.description, "For tying a length of thread between two coconuts")
		self.assertEqual(coco.tool_type, "needle")
		self.assertEqual(coco.shed, "parrot")
		self.assertEqual(coco.tool_pickup_arrangements, "Stop by anytime.")
		
	""" Deprecated: This functionality now belongs to 
		BorrowTransactions.
	"""
	@unittest.skip
	def test_get_all_user_tools(self):
		parrot = User.objects.get(username="Parrot")
		coco = Tool(
			name = "Coconut Threader", 
			owner = parrot, 
			description = "For tying a length of thread between two coconuts", 
			tool_type = "needle",
			tool_pickup_arrangements = "Stop by anytime.",
			available_date = timezone.now(),
			)
		coco.save()
		parrotTools = User.get_all_user_tools(parrot.id)
		self.assertTrue(parrotTools.filter(name="Coconut Threader").exists())
	

""" Test the API Routes in this app """
class UserApiTestCase(TestCase):
	
	def setUp(self):
		# Set up a Request Factory
		self.factory = RequestFactory()
		
		# Set up some Users
		self.john = User.create_new_user(
			u = 'John',
			p = 'hehehe', 
			zip_c = '00413', 
			e = 'ghostyTrickster@skaia.net',
			pn = '4134131996', 
			pa = 'mailbox',
			)
		self.john.save()
		
		# Mock session, where applicable
		self.mock_session = \
		{
			"user" : api.user_to_json(self.john)
		}
		
		# Session with no data
		self.empty_session = { }
		
		# Accurate login credentials
		self.good_login = \
		{
			'username' : self.john.username,
			'password' : "hehehe",
		}
		
		# New user form
		self.add_jade = \
		{
			'username' : "Jade",
			'password' : "tanglebuddies",
			'confirm_password' : "tanglebuddies",
			'zip_code' : '00413',
			'email' : "gardenGnostic@skaia.net",
			'phone_number' : "4131211995",
			'default_pickup_arrangements' : "time shenanigans",
		}
		
		# Change user form
		self.edit_john = \
		{
			'zip_code' : '00612',
			'email' : "ectoBiologist@skaia.net",
			'phone_number' : '4134132009',
			'default_pickup_arrangements' : "parcel pixys",
		}
	
	def test_getSelf(self):
		# Generate the request
		request = self.factory.get('/api/user/')
		request.session = self.mock_session
		response = api.user(request)
		
		# Did we get a clean response?
		self.assertEqual(response.status_code, 200)
		
		# Did we get the right data?
		response_data = json.loads(response.content.decode("utf-8"))
		self.assertEqual(response_data["id"], self.john.id)
		self.assertEqual(response_data["username"], self.john.username)
		self.assertEqual(response_data["zip_code"], self.john.zip_code)
		self.assertEqual(response_data["email"], self.john.email)
		self.assertEqual(response_data["phone_number"], 
			self.john.phone_number)
		self.assertEqual(response_data["default_pickup_arrangements"], 
			self.john.default_pickup_arrangements)
		self.assertEqual(response_data["is_shed_coordinator"],
			self.john.is_shed_coordinator)
		self.assertEqual(response_data["is_admin"], self.john.is_admin)
		
	def test_login(self):
		# Generate the request
		request = self.factory.post(
			path = '/api/login/',
			data = json.dumps(self.good_login), 
			content_type = "application/json",
			)
		request.session = self.empty_session
		response = api.login(request)
			
		# Did we get a clean response?
		self.assertEqual(response.status_code, 200)
		
		# Did we get the right data?
		response_data = json.loads(response.content.decode("utf-8"))
		self.assertEqual(response_data["id"], self.john.id)
		self.assertEqual(response_data["username"], self.john.username)
		self.assertEqual(response_data["zip_code"], self.john.zip_code)
		self.assertEqual(response_data["email"], self.john.email)
		self.assertEqual(response_data["phone_number"], 
			self.john.phone_number)
		self.assertEqual(response_data["default_pickup_arrangements"], 
			self.john.default_pickup_arrangements)
		self.assertEqual(response_data["is_shed_coordinator"],
			self.john.is_shed_coordinator)
		self.assertEqual(response_data["is_admin"], self.john.is_admin)
		
	def test_createNewUser(self):
		# Generate the request
		request = self.factory.post(
			path = '/api/user/',
			data = json.dumps(self.add_jade),
			content_type = "application/json",
			)
		request.session = self.empty_session
		response = api.user(request)
		
		# Did we get a clean response?
		self.assertEqual(response.status_code, 200)
		
		# Did we get the right data?
		response_data = json.loads(response.content.decode("utf-8"))
		self.assertEqual(response_data['username'], 
			self.add_jade['username'])
		self.assertEqual(response_data['zip_code'], 
			self.add_jade['zip_code'])
		self.assertEqual(response_data['email'], self.add_jade['email'])
		self.assertEqual(response_data['phone_number'], 
			self.add_jade['phone_number'])
		self.assertEqual(response_data['default_pickup_arrangements'], 
			self.add_jade['default_pickup_arrangements'])
			
		# We don't know the ID, but we know it has to be different.
		self.assertNotEqual(response_data['id'], self.john.id)
		# Only the first user in each zone should be the coordinator.
		self.assertNotEqual(response_data['is_shed_coordinator'], 
			self.john.is_shed_coordinator)
		# New users should not be admins by default.
		self.assertEqual(response_data['is_admin'], 
			False)
		
	def test_userProfileEdit(self):
		# Generate the request
		request = self.factory.put(
			path = '/api/user/',
			data = json.dumps(self.edit_john), 
			content_type = "application/json",
			)
		request.session = self.mock_session
		response = api.userById(request, self.john.id)
			
		# Did we get a clean response?
		self.assertIsNotNone(response)
		self.assertEqual(response.status_code, 200)
		
		# Did the data change?
		response_data = json.loads(response.content.decode("utf-8"))
		self.assertEqual(response_data["id"], self.john.id)
		self.assertEqual(response_data["username"], self.john.username)
		self.assertNotEqual(response_data["zip_code"], self.john.zip_code)
		self.assertNotEqual(response_data["email"], self.john.email)
		self.assertNotEqual(response_data["phone_number"], 
			self.john.phone_number)
		self.assertNotEqual(response_data["default_pickup_arrangements"], 
			self.john.default_pickup_arrangements)
		#self.assertEqual(response_data["is_shed_coordinator"],
		#	self.john.is_shed_coordinator)
		self.assertEqual(response_data["is_admin"], self.john.is_admin)
	
	@unittest.skip #not ready yet
	def test_deleteUserProfile(self):
		request = self.factory.delete('/api/user/:id')
	
	@unittest.skip #not ready yet
	def test_getUsersInZipcode(self):
		request = self.factory.get('/api/user/zip/:zip_code')
	
	@unittest.skip #not ready yet
	def test_changePassword(self):
		request = self.factory.put('/api/changePassword')
	
	@unittest.skip #not ready yet
	def test_logout(self):
		request = self.factory.get('/api/user/logout')
	
	@unittest.skip #not ready yet
	def test_getAdmins(self):
		request = self.factory.get('/api/admins')
		
	@unittest.skip #not ready yet
	def test_changeShedCoordinator(self):
		request = self.factory.put('/api/admin/shedCoordinator')
	
