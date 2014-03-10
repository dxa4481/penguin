from django.test import TestCase
from .models import *

""" Test the creation and usage of users and tools. """
class ToolTestCase(TestCase):
	def setUp(self):

		User.create_new_user('Parrot', 'password', '03545', 'polly@python.org', '1234567890', 'Pining for the fjords.')
		User.create_new_user('Swallow', 'password', '03545', 'african_swallow@python.org', '1234567890', 'Incapable of lifting a coconut.')
		User.create_new_user('Swallow', 'password', '03534', 'european_swallow@python.org', '1234567890', 'Capable of lifting a coconut.')

	""" Try to retrieve some objects from the database. """
	def test_query(self):
		pp = User.objects.all()[0]
		self.assertEqual(pp.__str__(), 'Parrot')
		
		afsw = User.objects.get(pk=2)
		self.assertEqual(afsw.username, 'Swallow')
		
		self.assertIsInstance(pp, User)
		self.assertNotIsInstance(afsw, Tool)



	""" Do objects compare to each other as expected? """
	def test_compare(self):
		eusw = User.objects.filter(username = 'Swallow')[0]
		eusw2 = User.objects.filter(username = 'Swallow')[0]
		afsw = User.objects.filter(username = 'Swallow')[1]

		self.assertIsNot(eusw, afsw)
		self.assertEqual(eusw, eusw2)

	""" Can users be modified? """
	def test_modify(self):
		eusw = User.objects.get(pk=2)
		afsw = User.objects.get(pk=3)
		self.assertEqual(eusw.username, afsw.username)
		self.assertNotEqual(eusw.email, afsw.email)

		eusw.update_user('Swallow', '1234567890', '03545', 'african_swallow@python.org', 'Actually Just Another African Swallow')
		self.assertEqual(eusw.username, afsw.username)
		self.assertEqual(eusw.email, afsw.email)

#	def test_obvious_true(self):
#		self.assertEqual("String", "String")
#		self.assertTrue(3.5 > -1)
#		self.assertIsNone(None)

#	def test_obvious_fail(self):
#		self.assertTrue(False)

