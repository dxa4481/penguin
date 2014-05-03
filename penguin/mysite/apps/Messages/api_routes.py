from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json 
import datetime
from ..Users.models import User
from .models import Message
from ...json_datetime import dt_to_milliseconds

"""Takes a message object and converts it to JSON
:param msg: Message object
:returns json-ified message object
"""
def message_to_json(msg):
	return_message = {"to_user_name":msg.to_user.username,
						"from_user_name":msg.from_user.username,
						"message":msg.message,
						"date":dt_to_milliseconds(msg.date),
						"has_been_read":msg.has_been_read}
	return return_message
	
@csrf_exempt
def message(request):
	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		m = Message.create_message(post_data['from_user_id'], post_data['to_user_id'], post_data['message'])
		return_message = message_to_json(m)
		return HttpResponse(json.dumps(return_message), content_type="application/json")

	if request.method == "PUT":
		put_data = json.loads(request.body.decode("utf-8"))
		m = Message.mark_message_read(put_data['message_id'])
		return_message = message_to_json(m)
		return HttpResponse(json.dumps(return_message), content_type="application/json")

@csrf_exempt
def sentMessage(request):
	if request.method == "GET":
		userID = request.session['user']['id']
		return_messages = []
		messages = Message.get_all_sent_messages(userID)
		for m in  messages:
			return_messages.append(message_to_json(m))
		return HttpResponse(json.dumps(return_messages), content_type="application/json")

@csrf_exempt
def receivedMessage(request):
	if request.method == "GET":
		userID = request.session['user']['id']
		return_messages = []
		messages = Message.get_all_received_messages(userID)
		for m in  messages:
			return_messages.append(message_to_json(m))
		return HttpResponse(json.dumps(return_messages), content_type="application/json")
