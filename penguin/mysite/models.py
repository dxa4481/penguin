from django.db import models

""" User object
"""
class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	area_code = models.CharField(max_length=5)
	email = models.EmailField(max_length=30)
	phone_number = models.CharField(max_length=10)
	is_shed_coordinator = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_community_shed = models.BooleanField(default=False)
	
	""" Constructor for a user entry
	:param u: username string
	:param p: password string
	:param ac: area code string
	:param e: email string (forced email field type)
	:param pn: phone number string
	"""
	def create_new_user(self, u, p, ac,	e, pn):
		u = User(username=u, password=p,
		sarea_code=ac, email=e, 
		phone_number=pn)
		u.save()
	
	""" Constructor for a community shed entry
	:param ac: area code, used as username as well
	"""
	def create_new_community_shed(self, ac):
		cs = User(username=ac, password="", 
		area_code=ac, email="", phone_number="",
		is_community_shed=True)
		cs.save()
	
	""" Returns a user based on user's ID
	:param userID: user's ID
	:return User object
	"""
	def get_user(userID):
		return User.objects.filter(pk=userID)
	
	""" Get a user ID
	:return user's ID
	"""
	def get_user_id(self):
		return self.id
	
	""" Promotes user object to admin status
	"""
	def promote_user_to_admin(self):
		self.is_admin = True;
		self.save()
	
	""" Demotes user object from admin status
	"""
	def demote_user_from_admin(self):
		self.is_admin = False
		self.save()
		
	""" Promotes user object to shed coordinator
	"""
	def promote_user_to_shed_coordinator(self):
		self.is_shed_coordinator = True
		self.save()
	
	""" Demotes user object from shed coordinator
	"""
	def demote_user_from_shed_coordinator(self):
		if(self.is_shed_coordinator)
			self.is_shed_coordinator = False;
	
	""" Returns an array(?) of all user's tools
	"""
	def get_all_user_tools(self):
		return self.tool_set.all()
	
	""" Deletes a user
	"""
	def delete_user(self):
		self.tool_set.all().delete()
		self.delete()

		
	

class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	owner = models.ForeignKey('User')
	is_available = models.BooleanField(default=True)
	description = models.CharField(max_length=250)
	type = models.CharField(max_length=30)
	
	""" Constructor to add a new tool
	:param n: name of tool
	:param o: owner ID
	:param d: description of tool
	:param t: type of tool
	"""
	def add_new_tool(self, n, o, d, t):
		t = Tool(owner=User.objects.get(pk=o), name=n,
		description=d, type=t)
		t.save()
	
	""" Deletes the given tool
	"""
	def delete_tool(self):
		self.delete()
	
	"""Sets a tool as unavailable
	"""
	def set_tool_unavailable(self):
		self.is_available = False
		self.save()
		
	""" Sets a tool as available
	"""
	def set_tool_available(self):
		self.is_available = True
		self.save()
		
	"""Checks if tool is available
	:return true if available, false otherwise
	"""
	def is_tool_available(self):
		if (self.is_available==True)
			return True
		else
			return False

	""" Get tool's owner's id
	:return owner's id
	"""
	def get_tool_owner(self):
		return owner.get_user_id()
	
	""" Return tool's ID
	"""
	def get_tool_id(self):
		return self.id
		
	""" Returns tool based on ID
	"""
	def get_tool(toolID):
		return Tool.objects.filter(pk=toolID)
		
		
class OwnTool(models.Model):
	id = models.AutoField(primary_key=True)
	owner = models.ForeignKey('User')
	tool = models.ForeignKey('Tool')
	
	"""Create a new tool ownership
	:param o: owner object
	:param t: tool object
	"""
	def add_new_tool_ownership(self, o, t):
		own = OwnTool(owner=User.get_user(o),
		tool=Tool.get_tool(t))
		own.save()
	
	""" Remove a tool ownership
	"""
	def remove_tool_ownership(self):
		self.delete()
		
	""" Return a tool ownership by id
	"""
	#Not implemented. What should this return?	
	def get_tool_ownership(id):
		return null
	
	"""Get a tool ownership's id
	:return id of tool ownership
	"""
	def get_tool_ownership_id(self):
		return self.id
		
class BorrowTransaction(models.Model):
	id = models.AutoField(primary_key=True)
	owner = models.ForeignKey('User')
	borrower = models.ForeignKey('User')
	tool = models.ForeignKey('Tool')
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
	def get_owner_borrow_transactions(ownerID):
		return BorrowTransaction.objects.filter(owner.id=ownerID)
		
	""" Gets a tool borrower's borrow transactions
	"""
	def get_borrower_borrow_transactions(borrowerID):
		return BorrowTransaction.objects.filter(borrower.id=borrowerID)
		
	
