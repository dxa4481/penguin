from models import *

class UserManager():
	def create_new_user(self, u, p, ac, e, pn):
		newuser = User(username=u, password=p,
		area_code=ac, email=e, 
		phone_number=pn)
		newuser.save()