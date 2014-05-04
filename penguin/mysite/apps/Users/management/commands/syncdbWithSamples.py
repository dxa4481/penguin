from mysite.apps.Users.models import User
from mysite.apps.Browse.models import BorrowTransaction
from mysite.apps.Tools.models import Tool
import datetime
from django.utils import timezone
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
import random


class Command(BaseCommand):
	def handle(self, *args, **options):
		try:
			call_command('flush', interactive=True)
		except:
			print("Couldn't flush, tables probably weren't built, building now")
		call_command('syncdb', interactive=True)
		User.create_new_user('Dan', 'password', '03545', 'dan@dan.com', '1234567890', "email me!")
		User.create_new_user('Andrew', 'password', '03545', 'andrew@andrew.com', '1234567890', "come to my house")
		User.create_new_user('Schmitty', 'password', '03545', 'schmitty@schmitty.com', '1234567890', "come to my work")
		User.create_new_user('Samantha', 'password', '03545', 'sam@sam.com', '1234567890', "knock twice, then once, then twice again")
		User.create_new_user('Nick', 'password', '03545', 'nick@nick.com', '1234567890', "use morse code on my door")
		User.promote_user_to_admin(1)

	
		
		Tool.create_new_tool('Drill 1', '1', 'A blue drill', 'drill', False, "email me!")
		Tool.create_new_tool('Drill 2', '1', 'An orange drill', 'drill', False, "knock on my door")
		Tool.create_new_tool('Drill 3', '1', 'A purple drill', 'drill', False, "find me at work")
		Tool.create_new_tool('Drill 4', '1', 'A green drill', 'drill', False, "find me at work")
		Tool.create_new_tool('Drill 5', '1', 'A yellow drill', 'drill', False, "find me at work")
		Tool.create_new_tool('Drill 6', '1', 'A black drill', 'drill', False, "find me at work")
		Tool.create_new_tool('Drill 7', '1', 'A brown drill', 'drill', False, "find me at work")
		Tool.create_new_tool('Screwdriver 8', '1', 'A green screwdriver', 'screwdriver', True, "email me!")
		Tool.create_new_tool('Screwdriver 9', '4', 'A purple screwdriver', 'screwdriver', True, "email me!")
		Tool.create_new_tool('Screwdriver 10', '3', 'A purple screwdriver', 'screwdriver', True, "email me!")
		
		avail_date = timezone.now() + datetime.timedelta(days=20)
		
		for i in range(0, 150):
			user_num = random.choice(range(1,5))
			name1 = random.choice(['Antimatter ', 'Autodynamic ', 'Catalytic ', 'Covalent ', 'Energized ', 'Gyromorphic ',
									'Maser ' ,'Neutronium ', 'Nuclear ','Subspace ' ,'Zero-point '])
			tool_type = random.choice(['Drill', 'Screwdriver', 'Hammer', 'Nailgun', 'Pliers', 'Wrench', 'Knife', 'Awl'])
			descrip = random.choice(['Red', 'Blue', 'Purple', 'Orange', 'Brown', 'Decrepit', 'Functional', 'Working', 'Broken', 'Bent', 'Shoddy'])
			in_comm_shed = random.choice([True, False, False, False])
			pickup_arrangement = random.choice(['send an email to me and wait for my reply', 'knock on my door three times, then once more', 
												'find me at work and tell my boss you are a doctor', 'call me over and over and over again', 
												'go bother my wife and tell her I am productive', 'go bother my husband and tell him to get back to work', 
												'drive through the wall and into my living room', 'kick in the door to my shed and take it', 
												'go around back of the house and find it in the garden'])
			if i==73:
				Tool.create_new_tool('Mr. Wobbles', '4', 'Hits the spot', 'Marital aid', False, 'come inside if you dont see the red pickup truck')
			Tool.create_new_tool(str(name1 + tool_type), user_num, str("A " + descrip + " " + tool_type), tool_type, in_comm_shed, pickup_arrangement)
			
			if (random.choice(range(10)) == 7):
				t = Tool.get_tool(i)
				b = User.get_user(user_num)
				borrow_message = random.choice(['I want this tool please' , 'Can I borrow this?', 'I promise I will give it back soon', 'I really need this', 
												'You are the best! Please let me use this?'])
				bt = BorrowTransaction.create_new_borrow_transaction(b, t, borrow_message, avail_date)
				BorrowTransaction.end_borrow_transaction(bt.id)
		
		avail_date = timezone.now() + datetime.timedelta(days=20)
		#request pending bt ID1
		b = User.get_user(2)
		t = Tool.get_tool(1)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "Can I haz this tool?", avail_date)
		#borrowing bt ID2
		t = Tool.get_tool(2)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "I want tool.", avail_date)
		BorrowTransaction.approve_borrow_transaction(bt.id)
		#rejected bt ID3
		t = Tool.get_tool(3)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "I wanta da tool.", avail_date)
		BorrowTransaction.reject_borrow_transaction(bt.id, "screw you")
		#return pending ID4
		t = Tool.get_tool(4)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "All your tool are belong to us.", avail_date)
		BorrowTransaction.request_end_borrow_transaction(bt.id)
		#returned transaction ID5
		t = Tool.get_tool(5)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "All your tool are belong to us.", avail_date)
		BorrowTransaction.end_borrow_transaction(bt.id)
		
		#make Andrew a shed coordinator
		User.promote_user_to_shed_coordinator(2)
		
		print("Added samples successfully!")	


