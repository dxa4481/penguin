from mysite.apps.Tools.models import *
#from mysite.apps.Browse.models import *

class popdb():
	
	def create_users(self):
		User.create_new_user('Dan', 'password', '03545', 'dan@dan.com', '1234567890')
		User.create_new_user('Andrew', 'password', '03545', 'dan@dan.com', '1234567890')
		User.create_new_user('Schmitty', 'password', '03545', 'dan@dan.com', '1234567890')
		User.create_new_user('Sam', 'password', '03545', 'dan@dan.com', '1234567890')
		User.create_new_user('Derpface', 'password', '03545', 'dan@dan.com', '1234567890')
	
	def create_tool(self):
		User.create_new_tool('1', 'Screwdriver 1', 'A blue screwdriver', 'screwdriver')
		User.create_new_tool('1', 'Screwdriver 2', 'A red screwdriver', 'screwdriver')
		User.create_new_tool('2', 'Screwdriver 3', 'A green screwdriver', 'screwdriver')
		User.create_new_tool('3', 'Screwdriver 4', 'A purple screwdriver', 'screwdriver')
		User.create_new_tool('2', 'Drill 1', 'A blue drill', 'drill')
		User.create_new_tool('1', 'Drill 2', 'An orange drill', 'drill')
		User.create_new_tool('2', 'Drill 3', 'A purple drill', 'drill')
		
	def create_bt(self):
		o = User.get_user(1)
		b = User.get_user(2)
		t = Tool.get_tool(1)
		BorrowTransaction.create_new_borrow_transaction(o, b, t)