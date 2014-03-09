from mysite.apps.Tools.models import *

User.create_new_user('Dan', 'password', '03545', 'dan@dan.com', '1234567890', "email me!")
User.create_new_user('Andrew', 'password', '03545', 'andrew@andrew.com', '1234567890', "come to my house")
User.create_new_user('Schmitty', 'password', '03545', 'schmitty@schmitty.com', '1234567890', "come to my work")
User.create_new_user('Sam', 'password', '03545', 'sam@sam.com', '1234567890', "knock twice, then once, then twice again")
User.create_new_user('Nick', 'password', '03545', 'nick@nick.com', '1234567890', "use morse code on my door")

User.create_new_tool('2', 'Screwdriver 3', 'A green screwdriver', 'screwdriver', "personal", "email me!")
User.create_new_tool('3', 'Screwdriver 4', 'A purple screwdriver', 'screwdriver', "personal", "email me!")
User.create_new_tool('2', 'Drill 1', 'A blue drill', 'drill', "personal", "email me!")
User.create_new_tool('1', 'Drill 2', 'An orange drill', 'drill', "personal", "knock on my door")
User.create_new_tool('2', 'Drill 3', 'A purple drill', 'drill', "community", "find me at work")
b = User.get_user(2)
t = Tool.get_tool(1)
BorrowTransaction.create_new_borrow_transaction(b, t)

