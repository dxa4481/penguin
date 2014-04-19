from django.db import models

from ..Users.models import User
from ..Tools.models import Tool

	

class BorrowTransaction(models.Model):
	id = models.AutoField(primary_key=True)
	borrower = models.ForeignKey(User)
	tool = models.ForeignKey(Tool)
	is_current_bt = models.BooleanField(default=True)
	in_community_shed = models.BooleanField(default=False)

	def __str__(self):
		return (str(self.id) + ' borrower: ' + self.borrower.username + ', tool: ' + self.tool.name)
	
	""" Create a new borrow transaction
	STATIC METHOD
	:param o: owner user
	:param b: borrower user
	:param t: tool
	:returns the ID of the borrow transaction that was created
	"""
	@staticmethod
	def create_new_borrow_transaction(b, t):
		bt = BorrowTransaction(borrower=b, tool=t)
		if bt.tool.in_community_shed:
			bt.in_community_shed=True
		bt.save()
		return bt.id

	""" Ends a borrow transaction
	STATIC METHOD
	:param btID: borrow transaction's ID
	"""
	@staticmethod
	def end_borrow_transaction(btID):
		bt = BorrowTransaction.get_borrow_transaction(btID)
		Tool.set_tool_available(bt.tool.id)
		bt.is_current_bt = False
		bt.save()

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
		return BorrowTransaction.objects.get(pk=btID)

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
		return BorrowTransaction.objects.get(tool=t, is_current_bt=True)
	
	""" Gets a tool borrower's borrow transactions
	:param borrowerID: The borrower user's ID
	STATIC METHOD
	"""
	@staticmethod
	def get_borrower_borrow_transactions(borrowerID):
		transactions = BorrowTransaction.objects.filter(borrower=User.get_user(borrowerID))
		return_transactions = []
		for transaction in transactions:
			print(transaction)
			if BorrowTransaction.is_current(transaction):
				return_transactions.append(transaction)
			else:
				print("setting false")
				transaction.is_current_bt=False
				transaction.save()
		return return_transactions

	""" Checks if a tool is currently available
	:param transaction: A borrow transaction object
	:returns true if a tool is currently being borrowed, false otherwise
	"""
	@staticmethod
	def is_current(transaction):
		return not Tool.is_tool_available(transaction.tool.id)

	""" Gets tools that a user owns that are being borrowed
	:param userID: user's ID that owns the tools
	:returns list of borrow transactions
	"""
	@staticmethod
	def get_borrow_transaction_user_owns(userID):
		owner = User.get_user(userID)
		return BorrowTransaction.objects.filter(tool__owner=owner, is_current_bt=True)