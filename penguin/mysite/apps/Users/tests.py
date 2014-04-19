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
		
	def test_get_all_user_tools(self):
		parrot = User.objects.get(username="Parrot")
		User.create_new_tool(parrot.id, "Coconut Threader", "For tying a length of thread between two coconuts", "needle", "parrot", "Stop by anytime.")
		parrotTools = User.get_all_user_tools(parrot.id)
		self.assertTrue(parrotTools.filter(name="Coconut Threader").exists())
