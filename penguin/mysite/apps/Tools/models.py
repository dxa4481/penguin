from django.db import models

#User = models.ForeignKey('Users.User')

""" User object
"""
class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	area_code = models.CharField(max_length=5)
	email = models.CharField(max_length=30)
	phone_number = models.CharField(max_length=10)
	is_shed_coordinator = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_community_shed = models.BooleanField(default=False)
	
	def __str__(self):
		return (str(self.id) + ':' + self.username)

		
	""" Constructor for a user entry
	STATIC METHOD
	:param u: username string
	:param p: password string
	:param ac: area code string
	:param e: email string (forced email field type)
	:param pn: phone number string
	"""
	@staticmethod
	def create_new_user(u, p, ac, e, pn):
		newuser = User(username=u, password=p,
		area_code=ac, email=e, 
		phone_number=pn)
		newuser.save()
		
	""" Constructor for a community shed entry
	STATIC METHOD
	:param ac: area code, used as username as well
	"""
	@staticmethod
	def create_new_community_shed(ac):
		cs = User(username=ac, password="", 
		area_code=ac, email="", phone_number="",
		is_community_shed=True)
		cs.save()
		
		
	""" Returns a user based on user's ID
	STATIC METHOD
	:param userID: user's ID
	:return User object
	"""
	@staticmethod
	def get_user(userID):
		return User.objects.get(pk=userID)
	

	@staticmethod
	def get_user_by_username(username_lookup):
		users = User.objects.filter(username=username_lookup)
		if(users.count() != 1):
			return False
			
		return users[0]	


	""" Promotes user object to admin status
	STATIC METHOD
	:param userID: user's ID
	"""
	@staticmethod
	def promote_user_to_admin(userID):
		u = User.get_user(userID)
		u.is_admin = True;
		u.save()
	
	""" Demotes user object from admin status
	STATIC METHOD
	:param userID: user's ID
	"""
	@staticmethod
	def demote_user_from_admin(userID):
		u = User.get_user(userID)
		u.is_admin = false;
		u.save()
	
	""" Promotes user object to shed coordinator
	STATIC METHOD
	:param userID: user's ID
	"""
	@staticmethod
	def promote_user_to_shed_coordinator(userID):
		u = User.get_user(userID)
		u.is_shed_coordinator = True;
		u.save()
	
	""" Demotes user object from shed coordinator
	STATIC METHOD
	:param userID: user's ID
	"""
	@staticmethod
	def demote_user_from_shed_coordinator(userID):
		u = User.get_user(userID)
		u.is_shed_coordinator = False;
		u.save()
		
	""" Checks if a user is an admin
	STATIC METHOD
	:param userID: user's ID
	"""
	@staticmethod
	def is_user_admin(userID):
		u = User.get_user(userID)
		return u.is_admin
		
	""" Checks if a user is a shed coordinator
	STATIC METHOD
	:param userID: user's ID
	"""
	@staticmethod
	def is_user_admin(userID):
		u = User.get_user(userID)
		return u.is_shed_coordinator
	
	""" Get a user ID
	:return user's ID
	"""
	def get_user_id(self):
		return self.id
		

	""" Deletes a user & all of their tools
	:param userID: user's ID
	"""
	@staticmethod
	def delete_user(userID):
		u = User.get_user(userID)
		u.delete()

		
	"""Add a new tool to tools, then relate it to this user
	:param userID: user's ID
	:param toolname: name of tool
    :param tooldescription: description of tool
    :param tooltype: type of tool
	"""
	@staticmethod
	def create_new_tool(userID, toolname, tooldescription, tooltype):
		u = User.get_user(userID)
		t = Tool.create_new_tool(toolname, u, tooldescription, tooltype)
		
	""" Returns an array(?) of all user's tools
	:param userID: user's ID
	"""
	def get_all_user_tools(userID):
		u = User.get_user(userID)
		tools = u.tool_set.all()
		return tools

class Tool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30)
	owner = models.ForeignKey('User')
	is_available = models.BooleanField(default=True)
	description = models.CharField(max_length=250)
	tool_type = models.CharField(max_length=30)
	
	def __str__(self):
		return (str(self.id) + ':' + self.name)

	""" Constructor to add a new tool
	STATIC METHOD
    :param toolname: name of tool
	:param toolowner: owner of the tool
    :param tooldescription: description of tool
    :param tooltype: type of tool
    :return The tool that was just added
    """
	@staticmethod
	def create_new_tool(toolname, toolowner, tooldescription, tooltype):
		t = Tool(name=toolname, owner=toolowner, description=tooldescription, tool_type=tooltype)
		t.save()
		return t
		
	""" Deletes the given tool
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def delete_tool(toolID):
		t = Tool.get_tool(toolID)
		t.delete()

	""" Returns tool based on ID
	"""
	@staticmethod
	def get_tool(toolID):
		return Tool.objects.get(pk=toolID)
		
		
	""" Return tool's ID
	"""
	def get_tool_id(self):
		return self.id

	"""Sets a tool as unavailable
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def set_tool_unavailable(toolID):
		t = Tool.get_tool(toolID)
		t.is_available = False
		t.save()

	""" Sets a tool as available
	STATIC METHOD
	:param toolID: tool's ID
	"""
	@staticmethod
	def set_tool_available(toolID):
		t = Tool.get_tool(toolID)
		t.is_available = True
		t.save()

	"""Checks if tool is available
	STATIC METHOD
	:param toolID: tool's ID
	:return true if available, false otherwise
	"""
	@staticmethod
	def is_tool_available(toolID):
		t = Tool.get_tool(toolID)
		return t.is_available

	""" Get tool's owner's id
	STATIC METHOD
	:param toolID: tool's ID
	:return owner's id
	"""
	@staticmethod
	def get_tool_owner(toolID):
		t = Tool.get_tool(toolID)
		return t.owner

class BorrowTransaction(models.Model):
	id = models.AutoField(primary_key=True)
	owner = models.ForeignKey('User', related_name='borrowtransaction_owner')
	borrower = models.ForeignKey('User', related_name='borrowtransaction_borrower')
	tool = models.ForeignKey('Tool')
	is_current = models.BooleanField(default=True)
	in_community_shed = models.BooleanField(default=False)

	def __str__(self):
		return (str(self.id) + ' owner:' + self.owner.username + ', borrower: ' + self.borrower.username + ', tool: ' + self.tool.name)
	
	""" Create a new borrow transaction
	STATIC METHOD
	:param o: owner user
	:param b: borrower user
	:param t: tool
	"""
	@staticmethod
	def create_new_borrow_transaction(o, b, t):
			bt = BorrowTransaction(owner=o,
			borrower=b, tool=t)
			Tool.set_tool_unavailable(t.get_tool_id())
			bt.save()

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

	""" Gets a tool owner's borrow transactions
	STATIC METHOD
	:param ownerID ID for owner of tool
	"""
	@staticmethod
	def get_owner_borrow_transactions(ownerID):
		return BorrowTransaction.objects.filter(owner=User.get_user(ownerID))

	""" Gets a tool borrower's borrow transactions
	STATIC METHOD
	"""
	@staticmethod
	def get_borrower_borrow_transactions(borrowerID):
		return BorrowTransaction.objects.filter(borrower=User.get_user(borrowerID))


