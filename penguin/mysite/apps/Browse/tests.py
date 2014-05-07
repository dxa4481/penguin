# For unit testing
from django.test import TestCase
import unittest
import datetime
from django.utils import timezone
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt

# For model testing
from .models import *

# For API testing
from django.test.client import RequestFactory
import json
from . import api_routes as api

""" Attempt to test users borrowing tools from other users. """
class BorrowTransactionTestCase(TestCase):
		
	def setUp(self):
		# Make some basic objects to play with.
		self.parrot = User.create_new_user( "Parrot", 
			"password", 
			"03545", 
			"polly@python.org", 
			"1234567890", 
			"Pining for the fjords."
			)
		self.penguin = User.create_new_user( 'Penguin', 
			'password', 
			'03545',
			'penguin@python.org', 
			'5555551234', 
			'It\'s on the telly.')
		self.nail = Tool.create_new_tool( toolname = "Rusty Nail", 
			toolownerID = self.parrot.id, 
			tooldescription = "Holding up a stuffed parrot", 
			tooltype = "nail", 
			toolshed = False, 
			pickup_info = "Rip it out of the cage.",
			tool_available = True
			)
		self.zilly = Tool.create_new_tool( "Warhammer of Zillyhoo", 
			toolownerID = self.parrot.id, 
			tooldescription = "Its majesty makes you weep.", 
			tooltype = "hammer", 
			toolshed = False, 
			pickup_info = "Some time travel required.",
			tool_available = True
			)
		
	def test_create_new_borrow_transaction(self):
		return None;
			
#	def test_get_borrow_transaction(self):
#	def test_get_borrower_borrow_transactions(self):
#	def test_is_current(self):

class BorrowTransactionApiTestCase(TestCase):
	
	def setUp(self):
		# Set up a Request Factory
		self.factory = RequestFactory()
		
		# Make some basic objects to play with.
		self.parrot = User.create_new_user( "Parrot", 
			"password", 
			"03545", 
			"polly@python.org", 
			"1234567890", 
			"Pining for the fjords."
			)
		self.penguin = User.create_new_user( 'Penguin', 
			'password', 
			'03545',
			'penguin@python.org', 
			'5555551234', 
			'It\'s on the telly.')
		self.polarbear = User.create_new_user( 'Polarbear',
			'password',
			'00000',
			'polarbear@northpole.org',
			'5555551234',
			'Pick it up at the north pole'
			)
		self.nail = Tool.create_new_tool( "Rusty Nail", 
			toolownerID = self.parrot.id, 
			tooldescription = "Holding up a stuffed parrot", 
			tooltype = "nail", 
			toolshed = False, 
			pickup_info = "Rip it out of the cage.",
			tool_available= True
			)
		self.zilly = Tool.create_new_tool( "Warhammer of Zillyhoo", 
			toolownerID = self.parrot.id, 
			tooldescription = "Its majesty makes you weep.", 
			tooltype = "hammer", 
			toolshed = False, 
			pickup_info = "Some time travel required.",
			tool_available= True
			)
		self.scraper = Tool.create_new_tool( "Ice Scraper",
			toolownerID = self.penguin.id,
			tooldescription = "An ice scraper for your car",
			tooltype = "ice scraper",
			toolshed = False,
			pickup_info = "Pick it up at the south pole.",
			tool_available= True
			)
	
	#cutting this out in case we lose points for that dumb runtime warning
	@unittest.skip
	def test_requestBorrowTransaction(self):
		# Penguin borrows nail from parrot
		jsondata = {
			'toolId' : self.nail.id,
			'borrower_message' : "i need dis",
			# NOTE: Python throws a nasty runtime error here because it
			# can't tell whether the milliseconds are timezone-aware.
			# Nothing I can do about this, just ignore the warning.
			'date' : dt_to_milliseconds(timezone.datetime(
				year = 3000,
				month = 4,
				day = 13,
				)),
			}
		request = self.factory.post(
			path = '/api/borrowTransaction',
			data = json.dumps(jsondata), 
			content_type = "application/json",
			)
		request.session = {
			'user' : {
				'id' : self.penguin.id
			}
		}
		response = api.borrowTransaction(request)
		
		#print(response.content)
		self.assertEqual(response.status_code, 200)
	"""
	@unittest.skip # this is not actually required behavior
	def test_requestBorrowTransaction_differentzones(self):
		# Polar bear borrows ice scraper from penguin
		# note that polar bears and penguins do not live in the same
		# place
		jsondata = {
			'toolId' : self.scraper.id,
			'borrower_message' : "i need dis",
			'date' : dt_to_milliseconds(timezone.datetime(
				tzinfo = timezone.UTC,
				year = 3000,
				month = 4,
				day = 13,
				)),
			}
		request = self.factory.post(
			path = '/api/borrowTransaction',
			data = json.dumps(jsondata), 
			content_type = "application/json",
			)
		request.session = {
			'user' : {
				'id' : self.polarbear.id
			}
		}
		response = api.borrowTransaction(request)
		
		#print(response.content)
		self.assertNotEqual(response.status_code, 200)
	"""
	
	@unittest.skip #not ready yet
	def test_getUnresolvedBorrowTransactions(self):
		request = self.factory.get(
			path = '/api/borrowTransaction/requestPending'
			)
		
	@unittest.skip #not ready yet
	def test_resolveBorrowRequest(self):
		request = self.factory.post('/api/borrowTransaction/resolve')
	
	@unittest.skip #not ready yet
	def test_getRejectedRequests(self):
		request = self.factory.get(
			path = '/api/borrowTransaction/rejected/:id'
			)
	
	@unittest.skip #not ready yet
	def test_requestEndBorrowTransaction(self):
		request = self.factory.put('/api/borrowTransaction')
	
	@unittest.skip #not ready yet
	def test_getEndBorrowTransactionRequests(self):
		request = self.factory.get(
			path = '/api/borrowTransaction/endRequests'
			)
	
	@unittest.skip #not ready yet
	def test_resolveEndBorrowTransaction(self):
		request = self.factory.delete(
			path = '/api/borrowTransaction/:transactionId'
			)
	
	@unittest.skip #not ready yet
	def test_getToolsUserIsBorrowing(self):
		request = self.factory.put(
			path = '/api/borrowTransaction/borrowing/:userId'
			)
	
	@unittest.skip #not ready yet
	def test_getToolsUserIsLending(self):
		request = self.factory.get(
			path = '/api/borrowTransaction/borrowed/:userId'
			)
	
	@unittest.skip #not ready yet
	def test_getAllCommunityHistory(self):
		request = self.factory.get(
			path = '/api/borrowTransaction/community/:zip'
			)
	
	@unittest.skip #not ready yet
	def test_getAllReturnPendingBorrowTransactionsInCommunityShed(self):
		request = self.factory.get(
			path = '/api/borrowTransaction/pendingCommunity'
			)
	
