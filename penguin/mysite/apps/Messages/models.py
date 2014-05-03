from django.db import models

from ..Users.models import User

class Message(models.Model):
	id = models.AutoField(primary_key=True)
	from_user = models.ForeignKey(User, related_name="from_user")
	to_user = models.ForeignKey(User, related_name="to_user")
	has_been_read = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	message = models.CharField(max_length=1000)
	
	def __str__(self):
		return (str(self.id) + ' from: ' + self.from_user.username + ', to: ' + self.to_user.username + ', message: ' + self.message)
	
	"""Creates a new message
	:param fromID: ID of user message is from
	:param toID: ID of user message is to
	:param msg: The message being sent
	:returns the Message object
	"""
	@staticmethod
	def create_message(fromID, toID, msg):
		m = Message(from_user=User.get_user(fromID), to_user=User.get_user(toID), message=msg)
		m.save()
		return m
	
	""" Gets a message based on ID
	:param msgID: The ID of the message to return
	:returns Message object related to ID
	"""
	@staticmethod
	def get_message(msgID):
		message_list = Message.objects.filter(pk=msgID)
		if (len(bt_list) == 0):
			return False
		else:
			return message_list[0]
	
	""" Marks a message as read
	:param msgID: The ID of the message to mark read
	"""
	@staticmethod
	def mark_message_read(msgID):
		m = Message.get_message(msgID)
		m.has_been_read = True
		m.save()
		return m
		
	"""Returns all messages user has sent
	:param fromID: ID of user message is from
	:returns list of all messages sent
	"""
	@staticmethod
	def get_all_sent_messages(fromID):
		fromUser = User.get_user(fromID)
		return Message.objects.filter(from_user=fromUser)
	
	"""Returns all messages user has received
	:param toID: ID of user message is to
	:returns list of all messages received
	"""
	@staticmethod
	def get_all_received_messages(toID):
		toUser = User.get_user(toID)
		return Message.objects.filter(to_user=toUser)
	
	