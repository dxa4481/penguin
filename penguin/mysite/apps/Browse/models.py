from django.db import models

from ..Users.models import User
from ..Tools.models import Tool

class BorrowTransaction(models.Model):
        id = models.AutoField(primary_key=True)
        owner = models.ForeignKey(User, related_name='borrowtransaction_owner')
        borrower = models.ForeignKey(User, related_name='borrowtransaction_borrower')
        tool = models.ForeignKey(Tool)
        is_current = models.BooleanField(default=True)
        in_community_shed = models.BooleanField(default=False)

        """ Create a new borrow transaction
        :param o: owner user ID
        :param b: borrower user ID
        :param t: tool ID
        """
        def add_new_borrow_transaction(self, o, b, t):
                bt = BorrowTransaction(owner=User.get_user(o),
                borrower=User.get_user(b),
                tool=Tool.get_tool(t))
                bt.tool.set_tool_unavailable()
                bt.tool.save()
                bt.save()

        """ Ends a borrow transaction
        """
        def end_borrow_transaction(self):
                tool.set_tool_available()
                is_current = False
                self.save()

        """ Removes a borrow transaction
                May be unnecessary?
        """
        def delete_borrow_transaction(self):
                self.delete()

        """ Gets a borrow transaction by ID
        :return Borrow Transaction filtered by ID
        """
        def get_borrow_transaction(btID):
                return BorrowTransaction.objects.filter(pk=btID)

        """ Gets a borrow transaction's ID
        :return borrow transaction's ID
        """
        def get_borrow_transaction_id(self):
                return self.id

        """ Gets a tool owner's borrow transactions
        :param ownerID ID for owner of tool
        """
        #def get_owner_borrow_transactions(ownerID):
                #return BorrowTransaction.objects.filter(owner.id=ownerID)

        """ Gets a tool borrower's borrow transactions
        """
        #def get_borrower_borrow_transactions(borrowerID):
                #return BorrowTransaction.objects.filter(borrower.id=borrowerID)

