from django.db import models

Tool = models.ForeignKey('Tools.Tool')

""" User object
"""
class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	area_code = models.CharField(max_length=5)
	email = models.CharField(max_length=30)
	phone_number = models.CharField(max_length=10)
	default_pickup_arrangements = models.CharField(max_length=50)
	is_shed_coordinator = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_community_shed = models.BooleanField(default=False)


	
	def __str__(self):
		return (self.username)

		
	""" Constructor for a user entry
	STATIC METHOD
	:param u: username string
	:param p: password string
	:param ac: area code string
	:param e: email string (forced email field type)
	:param pn: phone number string
	"""
	@staticmethod
	def create_new_user(u, p, ac, e, pn, pa):
		new_user = User(username=u, password=p,
		area_code=ac, email=e, 
		phone_number=pn, default_pickup_arrangements=pa)
		new_user.save()
		return new_user
		
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
		
	""" Updates a user's phone number, area code, and email 
	based on their username
	:param username_lookup: username to search for
	:param phone_number_new: new phone number to save
	:param area_code_new: new area code to save
	:param email_new: new email to save
	"""
	@staticmethod
	def update_user(username_lookup, password_new, phone_number_new, area_code_new, email_new, new_pickup_arrangements):
		u = User.get_user_by_username(username_lookup)
		u.password = password_new
		u.phone_number = phone_number_new
		u.area_code = area_code_new
		u.email = email_new
		u.default_pickup_arrangements = new_pickup_arrangements
		print("New password is " + u.password)
		u.save()
	    
	""" Returns a user based on user's ID
	STATIC METHOD
	:param userID: user's ID
	:return User object
	"""
	@staticmethod
	def get_user(userID):
		return User.objects.get(pk=userID)
	
	""" Gets a user by searching for username
	STATIC METHOD
	:param username_lookup: username to match in database
	:return User if exists, False otherwise
	"""
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
	def is_user_shed_coordinator(userID):
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
	def create_new_tool(userID, toolname, tooldescription, tooltype, shed, pickup_arrangements):
		u = User.get_user(userID)
		t = Tool.create_new_tool(toolname, u, tooldescription, tooltype, shed, pickup_arrangements)
		
	""" Returns an array(?) of all user's tools
	:param userID: user's ID
	"""
	def get_all_user_tools(userID):
		u = User.get_user(userID)
		tools = u.tool_set.all()
		return tools