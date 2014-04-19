from mysite.apps.Users.models import User
from mysite.apps.Browse.models import BorrowTransaction
from mysite.apps.Tools.models import Tool
import datetime
from django.utils import timezone

import os
import subprocess


def pop_db():
	User.create_new_user('Dan', 'password', '03545', 'dan@dan.com', '1234567890', "email me!")
	User.create_new_user('Andrew', 'password', '03545', 'andrew@andrew.com', '1234567890', "come to my house")
	User.create_new_user('Schmitty', 'password', '03545', 'schmitty@schmitty.com', '1234567890', "come to my work")
	User.create_new_user('Sam', 'password', '03545', 'sam@sam.com', '1234567890', "knock twice, then once, then twice again")
	User.create_new_user('Nick', 'password', '03545', 'nick@nick.com', '1234567890', "use morse code on my door")
	
	Tool.create_new_tool('Screwdriver 3', '1', 'A green screwdriver', 'screwdriver', False, "email me!")
	Tool.create_new_tool('Screwdriver 4', '4', 'A purple screwdriver', 'screwdriver', False, "email me!")
	Tool.create_new_tool('Drill 1', '3', 'A blue drill', 'drill', False, "email me!")
	Tool.create_new_tool('Drill 2', '1', 'An orange drill', 'drill', False, "knock on my door")
	Tool.create_new_tool('Drill 3', '2', 'A purple drill', 'drill', True, "find me at work")
	b = User.get_user(2)
	t = Tool.get_tool(1)
	BorrowTransaction.create_new_borrow_transaction(b, t)
	avail_date = timezone.now() + datetime.timedelta(days=20)
	Tool.set_tool_unavailable(t.id, avail_date)
	

def dia():
	try:
		print("trying to delete db")
		os.remove("./db.sqlite3")
		print("removed db")
	except:
		print("error removing")
	
	try:
		print("Trying to sync db")
		subprocess.call(["python3", "manage.py", "syncdb"]) 
		print("called syncdb")
		print("populating")
		pop_db()
		print("populated database")
	except:
		print("error in syncing/populating")
		
pop_db()