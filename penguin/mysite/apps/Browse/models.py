from django.db import models

from ..Users.models import User
from ..Tools.models import Tool

	

class BorrowTransaction(models.Model):
	id = models.AutoField(primary_key=True)
	borrower = models.ForeignKey(User)
	tool = models.ForeignKey(Tool)
	is_current = models.BooleanField(default=True)
	in_community_shed = models.BooleanField(default=False)

	def __str__(self):
		return (str(self.id) + ' borrower: ' + self.borrower.username + ', tool: ' + self.tool.name)
	
	""" Create a new borrow transaction
	STATIC METHOD
	:param o: owner user
	:param b: borrower user
	:param t: tool
	"""
	@staticmethod
	def create_new_borrow_transaction(b, t):
		bt = BorrowTransaction(borrower=b, tool=t)
		bt.save()
		return bt.id

	""" Ends a borrow transaction
	STATIC METHOD
	:param btID: borrow transaction's ID
	"""
	@staticmethod
	def end_borrow_transaction(btID):
		bt = BorrowTransaction.get_borrow_transaction(btID)
		bt.tool.set_tool_available()
		bt.is_current = False
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

	""" Gets a tool borrower's borrow transactions
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
				transaction.is_current=False
				transaction.save()
		return return_transactions

	@staticmethod
	def is_current(transaction):
		return not Tool.is_tool_available(transaction.tool.id)


