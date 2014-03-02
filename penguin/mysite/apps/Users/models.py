from django.db import models


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
		
	#INCOMPLETE
	""" Deletes a user
	:param userID: user's ID
	"""
	@staticmethod
	def delete_user(userID):
		u = User.get_user(userID)
		#delete all tools relating to user
		u.delete()
		
	#INCOMPLETE
	"""Add a new tool to tools, then relate it to this user
	:param userID: user's ID
	:param n: name of tool
	:param d: description of tool
	:param t: type of tool
	"""
	@staticmethod
	def create_new_tool(userID, n, d, tt):
		u = User.get_user(userID)
		t = Tool.create_new_tool(n, d, tt)
		OwnTool.create_new_tool_ownership(u, t)
		
	#INCOMPLETE
	""" Returns an array(?) of all user's tools
	"""
	def get_all_user_tools(self):
		ot = OwnTool.objects.filter(owner=self)
		tools = ot.tool_set
		return tools
