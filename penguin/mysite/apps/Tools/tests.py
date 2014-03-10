from django.test import TestCase

""" Test the creation and usage of users and tools. """
class ToolTestCase(TestCase):
	def setUp(self):
		# create a new User to run tests on.
		User.create_new_user('Barney', 'password', 03545, 'purpledinosaur@pbs.org', '1234567890', 'Use your imagination.')

#	def test_case(self):

	def test_obvious_true(self):
		self.assertEqual("String", "String")
		self.assertTrue(3.5 > -1)
		self.assertIsNone(None)

#	def test_obvious_fail(self):
#		self.assertTrue(False)

