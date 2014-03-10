from django.test import TestCase
from .models import *

""" Test the creation and usage of users and tools. """
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



##        def test_create_new_tool(self):
##                User.create_new_tool(42, "sledgehammer", "a sturdy sledgehammer", "hammer", "03545", "come captchalogue it.")
##                hammer = Tool.objects.get()
##                print(hammer)
                
##class ToolTestCase(TestCase):

##	""" Try to retrieve some objects from the database. """
##	def test_query(self):
##		pp = User.objects.all()[0]
##		self.assertEqual(pp.__str__(), 'Parrot')
##		
##		afsw = User.objects.get(pk=2)
##		self.assertEqual(afsw.username, 'Swallow')
##		
##		self.assertIsInstance(pp, User)
##		self.assertNotIsInstance(afsw, Tool)
##
##
##
##	""" Do objects compare to each other as expected? """
##	def test_compare(self):
##		eusw = User.objects.filter(username = 'Swallow')[0]
##		eusw2 = User.objects.filter(username = 'Swallow')[0]
##		afsw = User.objects.filter(username = 'Swallow')[1]
##
##		self.assertIsNot(eusw, afsw)
##		self.assertEqual(eusw, eusw2)
##
##	""" Can users be modified? """
##	def test_modify(self):
##		eusw = User.objects.get(pk=2)
##		afsw = User.objects.get(pk=3)
##		self.assertEqual(eusw.username, afsw.username)
##		self.assertNotEqual(eusw.email, afsw.email)
##
##		eusw.update_user('Swallow', '1234567890', '03545', 'african_swallow@python.org', 'Actually Just Another African Swallow')
##		self.assertEqual(eusw.username, afsw.username)
##		self.assertEqual(eusw.email, afsw.email)

#	def test_obvious_true(self):
#		self.assertEqual("String", "String")
#		self.assertTrue(3.5 > -1)
#		self.assertIsNone(None)

#	def test_obvious_fail(self):
#		self.assertTrue(False)

