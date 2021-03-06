from django.db import models
from django.db.models import Q

from ..Users.models import User
from ..Tools.models import Tool

	

class BorrowTransaction(models.Model):
	id = models.AutoField(primary_key=True)
	borrower = models.ForeignKey(User)
	tool = models.ForeignKey(Tool)
	is_current_bt = models.BooleanField(default=True)
	in_community_shed = models.BooleanField(default=False)
	owner_message = models.CharField(max_length=250)
	borrower_message = models.CharField(max_length=250)
	status = models.CharField(max_length=30)

	def __str__(self):
		return (str(self.id) + ' borrower: ' + self.borrower.username + ', tool: ' + self.tool.name)
	
	""" Create a new borrow transaction
	STATIC METHOD
	:param b: borrower user
	:param t: tool
	:param borrow_message: borrower's message to the tool owner
	:returns the ID of the borrow transaction that was created
	"""
	@staticmethod
	def create_new_borrow_transaction(b, t, borrow_message, rent_date):
		bt = BorrowTransaction(borrower=b, tool=t, borrower_message=borrow_message, owner_message="", status="borrow request pending")
		if bt.tool.in_community_shed:
			bt.in_community_shed=True
			bt.status = "borrowing"
		Tool.set_tool_unavailable(bt.tool.id, rent_date)
		bt.save()
		return bt

	""" Approve a borrow transaction request
	:param btID: borrow transaction's ID
	:returns the borrow transaction object
	"""
	@staticmethod
	def approve_borrow_transaction(btID, own_msg):
		bt = BorrowTransaction.get_borrow_transaction(btID)
		bt.owner_message = own_msg
		bt.status = "borrowing"
		bt.save()
		return bt
		
	""" Rejects a borrow transaction request
	:param btID: borrow transaction's ID
	:param ownerMessage: owner's rejection message
	:returns the borrow transaction object
	"""
	@staticmethod
	def reject_borrow_transaction(btID, ownerMessage):
		bt = BorrowTransaction.get_borrow_transaction(btID)
		bt.owner_message = ownerMessage
		bt.status = "rejected"
		bt.is_current_bt=False
		Tool.set_tool_available(bt.tool.id)
		bt.save()
		return bt
		
	""" Request to return a tool and end a borrow transaction
	:param btID: borrow transaction's ID
	:returns the borrow transaction object
	"""
	def request_end_borrow_transaction(btID):
		bt = BorrowTransaction.get_borrow_transaction(btID)
		bt.status = "borrow return pending"
		bt.save()
		return bt
		
	""" Ends a borrow transaction
	STATIC METHOD
	:param btID: borrow transaction's ID
	"""
	@staticmethod
	def end_borrow_transaction(btID):
		bt = BorrowTransaction.get_borrow_transaction(btID)
		Tool.set_tool_available(bt.tool.id)
		bt.is_current_bt = False
		bt.status = "returned"
		bt.save()
		return bt

	""" Removes a borrow transaction
	STATIC METHOD
	May be unnecessary?
	"""
	@staticmethod
	def delete_borrow_transaction(btID):
		bt = BorrowTransaction.get_borrow_transaction(btID)
		bt.delete()

	""" Gets a borrow transaction by ID
	STATIC METHOD
	:return Borrow Transaction filtered by ID
	"""
	@staticmethod
	def get_borrow_transaction(btID):
		bt_list = BorrowTransaction.objects.filter(pk=btID)
		if (len(bt_list) == 0):
			return False
		else:
			return bt_list[0]

	""" Gets a borrow transaction's ID
	:return borrow transaction's ID
	"""
	def get_borrow_transaction_id(self):
		return self.id
		
	""" Gets the current borrow transaction for a tool
	:param toolID: The tool ID pertaining to the borrow transaction
	:returns borrow transaction ID
	"""
	@staticmethod
	def get_current_borrow_transaction_by_tool(toolID):
		t = Tool.get_tool(toolID)
		return BorrowTransaction.objects.get(tool=t, status="borrowing")
	
	""" Gets a tool borrower's borrow transactions
	:param borrowerID: The borrower user's ID
	STATIC METHOD
	"""
	@staticmethod
	def get_borrower_borrow_transactions(borrowerID):
		transactions = BorrowTransaction.objects.filter(borrower=User.get_user(borrowerID))
		return_transactions = []
		for transaction in transactions:
			if BorrowTransaction.is_current(transaction):
				return_transactions.append(transaction)
		return return_transactions

	""" Checks if a tool is currently available
	:param transaction: A borrow transaction object
	:returns true if a tool is currently being borrowed, false otherwise
	"""
	@staticmethod
	def is_current(transaction):
		if (transaction.status == "borrowing") or (transaction.status == "borrow request pending") or (transaction.status == "borrow return pending"):
			return True
		else:
			return False


	""" Gets tools that a user owns that are being borrowed
	:param userID: user's ID that owns the tools
	:returns list of borrow transactions
	"""
	@staticmethod
	def get_borrow_transaction_user_owns(userID):
		owner = User.get_user(userID)
		bt = BorrowTransaction.get_unresolved_borrow_transactions(userID)
		#return BorrowTransaction.objects.filter(tool__owner=owner)
		return BorrowTransaction.objects.filter(tool__owner=owner, status="borrowing")
		
	""" Gets all BT with a status of rejected
	:param userID: Borrower's user ID
	:return list of borrow transactions
	"""
	@staticmethod
	def get_rejected_borrow_transactions(userID):
		borr = User.get_user(userID)
		return BorrowTransaction.objects.filter(borrower=borr, status="rejected")
	
	""" Gets all BT with status 'borrow request pending', 'borrowing', or 'borrow return pending'
	:param userID: Borrower's user ID
	:return list of borrow transactions
	"""
	@staticmethod
	def get_unresolved_borrow_transactions(userID):
		return BorrowTransaction.objects.filter(tool__owner=User.get_user(userID), status="borrow request pending")
		
	""" Gets all BT with a status of "borrow return pending"
	:param userID: Borrower's user ID
	:return list of borrow transactions
	"""
	@staticmethod
	def get_return_pending_borrow_transactions(userID):
		user = User.get_user(userID)
		return BorrowTransaction.objects.filter(tool__owner=user, status="borrow return pending")
		
	""" Gets a request pending borrow transaction for a tool
	:param toolID: The tool ID pertaining to the borrow transaction
	:returns borrow transaction ID
	"""
	@staticmethod
	def get_request_pending_borrow_transaction_by_tool(toolID):
		t = Tool.get_tool(toolID)
		return BorrowTransaction.objects.get(tool=t, status="borrow request pending")
	
	""" Gets an unresolved borrow transaction for a tool
	:param toolID: The tool ID pertaining to the borrow transaction
	:returns borrow transaction ID
	"""
	@staticmethod
	def get_unresolved_borrow_transaction_by_tool(toolID):
		t = Tool.get_tool(toolID)
		bt = BorrowTransaction.objects.filter(Q(tool=t) & (Q(status="borrow request pending") | Q(status="borrowing") | Q(status="borrow return pending")))
		if (len(bt) == 0):
			return False
		else:
			return bt[0]


	@staticmethod
	def get_all_community_history(zip_code):
		all_communities = BorrowTransaction.objects.filter(tool__in_community_shed=True)
		just_in_zip = []
		for borrowTransaction in all_communities:
			if(borrowTransaction.tool.owner.zip_code == zip_code):
				just_in_zip.append(borrowTransaction)
		return just_in_zip
	"""Gets all return pending transactions in a community shed
	:param zip_c: The zip code for the community shed
	:returns list of borrow transactions
	"""
	@staticmethod
	def get_all_return_pending_in_community_shed(zip_c):
		all_communities = BorrowTransaction.objects.filter(status="borrow return pending", tool__in_community_shed=True)
		just_in_zip = []
		for borrowTransaction in all_communities:
			if(borrowTransaction.tool.owner.zip_code == zip_c):
				just_in_zip.append(borrowTransaction)
		return just_in_zip
