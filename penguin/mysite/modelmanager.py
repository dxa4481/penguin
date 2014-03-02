from mysite.database.models import *

class UserManager():
	
	""" Constructor for a user entry
	:param u: username string
	:param p: password string
	:param ac: area code string
	:param e: email string (forced email field type)
	:param pn: phone number string
	"""
	def create_new_user(self, u, p, ac, e, pn):
		newuser = User(username=u, password=p,
		area_code=ac, email=e, 
		phone_number=pn)
		newuser.save()
		
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
	def get_user(self, userID):
		return User.objects.get(pk=userID)
		
	""" Promotes user object to admin status
	:param userID: user's ID
	"""
	def promote_user_to_admin(self, userID):
		u = self.get_user(userID)
		u.is_admin = True;
		u.save()
	
	""" Demotes user object from admin status
	:param userID: user's ID
	"""
	def demote_user_from_admin(self, userID):
		u = self.get_user(userID)
		u.is_admin = false;
		u.save()
		
	""" Promotes user object to shed coordinator
	:param userID: user's ID
	"""
	def promote_user_to_shed_coordinator(self, userID):
		u = self.get_user(userID)
		u.is_shed_coordinator = True;
		u.save()
	
	""" Demotes user object from shed coordinator
	:param userID: user's ID
	"""
	def demote_user_from_shed_coordinator(self, userID):
		u = self.get_user(userID)
		u.is_shed_coordinator = False;
		u.save()
		
	""" Checks if a user is an admin
	:param userID: user's ID
	"""
	def is_user_admin(self, userID):
		u = self.get_user(userID)
		return u.is_admin
		
	""" Checks if a user is a shed coordinator
	:param userID: user's ID
	"""
	def is_user_admin(self, userID):
		u = self.get_user(userID)
		return u.is_shed_coordinator
	
	#INCOMPLETE
	""" Deletes a user
	:param userID: user's ID
	"""
	def delete_user(self, userID):
		u = self.get_user(userID)
		#delete all tools relating to user
		u.delete()
		
	#INCOMPLETE
	"""Add a new tool to tools, then relate it to this user
	:param userID: user's ID
	:param n: name of tool
	:param d: description of tool
	:param t: type of tool
	"""
	def add_new_tool(self, userID, n, d, t):
		u = self.get_user(userID)
		tm = ToolManager()
		t = tm.add_new_tool(n, d, t)
		OwnTool.add_new_tool_ownership(self, t)
		
	#INCOMPLETE
	""" Returns an array(?) of all user's tools
	"""
	def get_all_user_tools(self):
		ot = OwnTool.objects.filter(owner=self)
		tools = ot.tool_set
		return tools
	