from django.db import models
from hashlib import sha512
import uuid
from random import getrandbits

""" User object
"""
class User(models.Model):
	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30)
	hashed_password = models.CharField(max_length=512)
	zip_code = models.CharField(max_length=5)
	email = models.CharField(max_length=30)
	phone_number = models.CharField(max_length=10)
	default_pickup_arrangements = models.CharField(max_length=50)
	is_shed_coordinator = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	salt = models.CharField(max_length=256)

	
	def __str__(self):
		return (self.username)


	def verify_password(self, password):
		return(sha512(password.encode('utf-8') + self.salt.encode('utf-8')).hexdigest() == self.hashed_password)
		
	""" Constructor for a user entry
	STATIC METHOD
	:param u: username string
	:param p: password string
	:param zip: zip code string
	:param e: email string (forced email field type)
	:param pn: phone number string
	:return returns the user that was just created
	"""
	@staticmethod
	def create_new_user(u, p, zip_c, e, pn, pa):
		salt = uuid.uuid4().hex
		hashed_pw = sha512(p.encode('utf-8') + salt.encode('utf-8')).hexdigest()
		new_user = User(username=u, hashed_password=hashed_pw,
		zip_code=zip_c, email=e, 
		phone_number=pn, default_pickup_arrangements=pa, salt=salt)
		new_user.save()
		return new_user
		
		
	""" Updates a user's phone number, zip code, and email 
	based on their username
	:param username_lookup: username to search for
	:param phone_number_new: new phone number to save
	:param zip_code_new: new zip code to save
	:param email_new: new email to save
	:return the user that is being updated
	"""
	@staticmethod
	def update_user(username_lookup, phone_number_new, zip_code_new, email_new, new_pickup_arrangements):
		u = User.get_user_by_username(username_lookup)
		u.phone_number = phone_number_new
		u.zip_code = zip_code_new
		u.email = email_new
		u.default_pickup_arrangements = new_pickup_arrangements
		u.save()
		return u
	
	"""Updates a user's password
	:param userID: the user's ID
	:param password: the password to change to
	"""
	@staticmethod
	def update_password(userID, password):
		u = User.get_user(userID)
		u.salt = uuid.uuid4().hex
		u.hashed_password = sha512(password.encode('utf-8') + u.salt.encode('utf-8')).hexdigest()
		u.save()
	
	""" Returns a user based on user's ID
	STATIC METHOD
	:param userID: user's ID
	:return User object
	"""
	@staticmethod
	def get_user(userID):
		user_list = User.objects.filter(pk=userID)
		if (len(user_list) == 0):
			return False
		else:
			return user_list[0]
	
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
		u.is_admin = False;
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
		
		
	""" Deletes a user & all of their tools
	:param userID: user's ID
	"""
	@staticmethod
	def delete_user(userID):
		u = User.get_user(userID)
		u.delete()
		
	
	""" Returns all users in a certain zipcode
	:param zip: zip code to search for
	:return List of all users in the zip code
	"""
	@staticmethod
	def get_user_by_zip_code(zip_c):
		return User.objects.filter(zip_code=zip_c)
		
	""" Gets all admins for the system
	return list of all admin users
	"""
	@staticmethod
	def get_all_admins():
		return User.objects.filter(is_admin=True)
		
	""" Gets the shed coordinator for the given share zone
	:param zip_c: the zip code to search in
	:returns User object who is shed coordinator
	"""
	@staticmethod
	def get_shed_coordinator_for_zip(zip_c):
		return User.objects.get(is_shed_coordinator=True, zip_code=zip_c)
		
	""" Checks if a shed coord exists for given share zone
	:param zip_c: zip code to search in
	:returns True if shed coord exists, False otherwise
	"""
	@staticmethod 
	def does_shed_coord_exist(zip_c):
		u = User.objects.filter(is_shed_coordinator=True, zip_code=zip_c)
		if (len(u) == 1):
			return True
		else:
			return False