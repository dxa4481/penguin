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
		
		#make Dan an admin
		User.promote_user_to_admin(1)
		#make Andrew a shed coordinator
		User.promote_user_to_shed_coordinator(1)
		
		avail_date = timezone.now() + datetime.timedelta(days=20)
		
		for i in range(0, 150):
			print("Inserting samples. " + str(round(((i+1)/150)*100, 2)) + " percent complete.")
			user_num = random.choice(range(1,5))
			name1 = random.choice(['Antimatter ', 'Autodynamic ', 'Catalytic ', 'Covalent ', 'Energized ', 'Gyromorphic ',
									'Maser ' ,'Neutronium ', 'Nuclear ','Subspace ' ,'Zero-point ', 'Ingenuitive ',
						'Multi-Platform ', 'NP-Complete ', 'Revolutionary ', 'Regression ', 'Recursive ', 'Crowd-Sourced ', 
						'Thought Based ', 'Web 2.0 ', 'Middleware ', 'Innovative ', 'Beta ', 'Alpha ', 'Synergetic ', 'Aggregating ',
						'Big O ', 'Cloud Based ', 'Cloud Service ', 'Service Oriented ', 'Reactive ', 'Net Neutral ', 'Agile ',
						'Plug-n-play ', 'Open Source ', 'Location Aware ', 'Bionic ', 'Cosmic ', 'Ionic ', 'Quantum '])
			tool_type = random.choice(['Drill', 'Screwdriver', 'Hammer', 'Nailgun', 'Pliers', 'Wrench', 'Knife', 'Awl', 'Web Platform',
							'3D Printer', 'Recursion', 'Middleware', 'Innovator', 'Synergizer', 'Mallet', 'Sander', 'Lathe', 'Crowbar',
							'Cloud Software', 'Architecture', 'Paradigm', 'Clamp', 'Utility Curve'])
			descrip = random.choice(['Red', 'Blue', 'Purple', 'Orange', 'Brown', 'Decrepit', 'Functional', 'Working', 'Broken', 'Bent', 'Shoddy'])
			in_comm_shed = random.choice([True, False, False, False])
			pickup_arrangement = random.choice(['send an email to me and wait for my reply', 'knock on my door three times, then once more', 
												'find me at work and tell my boss you are a doctor', 'call me over and over and over again', 
												'go bother my wife and tell her I am productive', 'go bother my husband and tell him to get back to work', 
												'drive through the wall and into my living room', 'kick in the door to my shed and take it', 
												'go around back of the house and find it in the garden'])
			if i==73:
				Tool.create_new_tool('Mr. Wobbles', '4', 'Hits the spot', 'Marital aid', False, 'come inside if you dont see the red pickup truck', True)
			Tool.create_new_tool(str(name1 + tool_type), user_num, str("A " + descrip + " " + tool_type), tool_type, in_comm_shed, pickup_arrangement, True)
			
			bt_choice = random.choice(range(10))
			if (bt_choice >= 6):
				t = Tool.get_tool(i)
				b = User.get_user(user_num)
				if (t != False and t.owner != b):
					borrow_message = random.choice(['I want this tool please' , 'Can I borrow this?', 'I promise I will give it back soon', 'I really need this', 
													'You are the best! Please let me use this?'])
					bt = BorrowTransaction.create_new_borrow_transaction(b, t, borrow_message, avail_date)
					if (bt_choice == 6):
						BorrowTransaction.approve_borrow_transaction(bt.id, "I sanction this transaction!")
						BorrowTransaction.end_borrow_transaction(bt.id)
					elif (bt_choice == 7):
						BorrowTransaction.approve_borrow_transaction(bt.id, "I sanction this transaction!")
					elif (bt_choice == 8):
						BorrowTransaction.approve_borrow_transaction(bt.id, "I sanction this transaction!")
						BorrowTransaction.request_end_borrow_transaction(bt.id)
		
		avail_date = timezone.now() + datetime.timedelta(days=20)
		
		Tool.create_new_tool("Bionic Mallet", 1, "A handy dandy bionic mallet", "Hammer", False, "Come pick it up!", True)
		Tool.create_new_tool("Cosmic Sander", 1, "Sand things to spacedust", "Sander", False, "Call me!", True)
		Tool.create_new_tool("Cybermeasure", 1, "Measures in lightyears", "Ruler", False, "Call me!", True)
		Tool.create_new_tool("Dimensional Oscillolathe", 1, "Out of this world!", "Lathe", False, "Get it while it's hot", True)
		Tool.create_new_tool("Techno Chisel", 1, "It's smarter than you", "Chisel", False, "Come get it", True)
		
		dan_tool_list = Tool.get_tool_by_owner(1)
		list_length = len(dan_tool_list)
		
		#request pending bt ID1
		b = User.get_user(2)
		t = Tool.get_tool(dan_tool_list[list_length-1].id)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "Can I haz this tool?", avail_date)
		#borrowing bt ID2
		t = Tool.get_tool(dan_tool_list[list_length-2].id)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "I want tool.", avail_date)
		BorrowTransaction.approve_borrow_transaction(bt.id, "Sure, go ahead I guess. I didn't want that tool anyway.")
		#rejected bt ID3
		t = Tool.get_tool(dan_tool_list[list_length-3].id)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "I wanta da tool.", avail_date)
		BorrowTransaction.reject_borrow_transaction(bt.id, "Forget you, you can't have it")
		#return pending ID4
		t = Tool.get_tool(dan_tool_list[list_length-4].id)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "All your tool are belong to us.", avail_date)
		BorrowTransaction.approve_borrow_transaction(bt.id, "Sure, go ahead I guess. I didn't want that tool anyway.")
		BorrowTransaction.request_end_borrow_transaction(bt.id)
		#returned transaction ID5
		t = Tool.get_tool(dan_tool_list[list_length-5].id)
		bt = BorrowTransaction.create_new_borrow_transaction(b, t, "All your tool are belong to us.", avail_date)
		BorrowTransaction.approve_borrow_transaction(bt.id, "Sure, go ahead I guess. I didn't want that tool anyway.")
		BorrowTransaction.end_borrow_transaction(bt.id)
		

		
		print("Added samples successfully!")	


