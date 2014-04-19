from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json 
import datetime
from .models import User
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt



@csrf_exempt
def user(request):
	"""

	"""
	if request.method == 'GET':
		print(request.session['user'])
		u_id = request.session['user']['id']
		print(u_id)
		user = User.get_user(u_id)
		print(user)
		return_user = { "id": user.id,
				"username": user.username,
				"area_code": user.area_code,
				"email": user.email,
				"phone_number": user.phone_number,
				"default_pickup_arrangements": user.default_pickup_arrangements,
				"is_shed_coordinator": user.is_shed_coordinator,
				"is_admin": user.is_admin }
		print(return_user)
		return HttpResponse(json.dumps(return_user), content_type="application/json")
	"""
		username already exists
		password mismatch
		invalid email
		invalid zipcode
		invalid phone number
	"""
	if request.method == 'POST':
		post_data = json.loads(request.body.decode("utf-8"))
		new_user = User.create_new_user(post_data["username"],
						post_data["password"],
						post_data["area_code"],
						post_data["email"],
						post_data["phone_number"],
						post_data["default_pickup_arrangements"])
		return_user = { "id": new_user.id,
				"username": new_user.username,
				"area_code": new_user.area_code,
				"email": new_user.email,
				"phone_number": new_user.phone_number,
				"default_pickup_arrangements": new_user.default_pickup_arrangements,
				"is_shed_coordinator": new_user.is_shed_coordinator,
				"is_admin": new_user.is_admin }
		request.session['user'] = return_user
		print(request.session['user'])
		return HttpResponse(json.dumps(return_user), content_type="application/json")
	"""
		password mismatch
		invalid zipcode
		invalid email
		invalid phone number
	"""
	if request.method == 'PUT':
		put_data = json.loads(request.body.decode("utf-8"))
		print(put_data)
		User.update_user(request.session['user']['username'],
				put_data['password'],
				put_data['phone_number'],
				put_data['area_code'],
				put_data['email'],
				put_data['default_pickup_arrangements'])
		user = User.get_user_by_username(request.session['user']["username"])
		return_user = {	"id": user.id,
				"username": user.username,
				"area_code": user.area_code,
				"email": user.email,
				"phone_number": user.phone_number,
				"default_pickup_arrangements": user.default_pickup_arrangements,
				"is_shed_coordinator": user.is_shed_coordinator,
				"is_admin": user.is_admin }
		print(return_user)
		request.session['user'] = return_user
		print(request.session['user'])
		return HttpResponse(json.dumps(return_user), content_type="application/json")

@csrf_exempt
def userById(request, user_id):
	"""
	^/api/user/:id DELETE
	Known risks:
	  * Can delete any user, even if not logged in as them.
	  * Can delete users with tools checked out.
	  * Can delete users checking tools out.
	"""
	if request.method == "DELETE":
		try:
			User.delete_user(user_id)
			returnmsg = { 'success': True }
		except:
			returnmsg = { 'success': False }
			 
		return HttpResponse(json.dumps(returnmsg), content_type="application/json")

@csrf_exempt
def login(request):
	"""
		If username and password not in body
		if username not found
		if password incorrect
	"""
	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		user = User.get_user_by_username(post_data['username'])
		return_user = {"id": user.id, "username" : user.username, "area_code": user.area_code, "email": user.email, "phone_number": user.phone_number, "default_pickup_arrangements": user.default_pickup_arrangements, "is_shed_coordinator": user.is_shed_coordinator, "is_admin":user.is_admin}
		request.session['user'] = return_user
		print(request.session['user'])
		return HttpResponse(json.dumps(return_user), content_type="application/json")

