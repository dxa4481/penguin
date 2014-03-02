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

	""" Get a user ID
	:return user's ID
	"""
	def get_user_id(self):
		return self.id