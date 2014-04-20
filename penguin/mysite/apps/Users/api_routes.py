from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json 
import datetime
from .models import User
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt
from django.core.validators import validate_email, MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError


@csrf_exempt
def user(request):
	"""

	"""
	if request.method == 'GET':
		u_id = request.session['user']['id']
		user = User.get_user(u_id)
		return_user = { "id": user.id,
				"username": user.username,
				"zip_code": user.zip_code,
				"email": user.email,
				"phone_number": user.phone_number,
				"default_pickup_arrangements": user.default_pickup_arrangements,
				"is_shed_coordinator": user.is_shed_coordinator,
				"is_admin": user.is_admin }
		return HttpResponse(json.dumps(return_user), content_type="application/json")
	"""
		username already exists
		password mismatch
		invalid email
		invalid zipcode
		invalid phone number
		Missing Fields
	"""
	if request.method == 'POST':
		post_data = json.loads(request.body.decode("utf-8"))
		
		# if username already exists -- error 409
		if( User.get_user_by_username(post_data["username"]) != False ):
			error = { "error": "Username already exists" }
			return HttpResponse(json.dumps(error), content_type ="application/json", status=409)
		# if password doesn't match confirm password -- error 400
		if( post_data["password"] != post_data["confirm_password"] ):
			error = {"error": "passwords do not match!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# if email not a valid email address -- error 400
		try:
			validate_email( post_data["email"] )
		except ValidationError:
			error = {"error": "You entered an invalid email address!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# if zipcode not a valid zipcode -- error 400
		if( len(post_data["zip_code"]) != 5 ):
			error = {"error": "You entered an invalid zip code!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		try:
			is_int = int(post_data["zip_code"])
		except ValueError:
			error = {"error": "You entered an invalid zip code!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# if phone number not a valid phone number -- error 400
		if( validate_phone_number( post_data["phone_number"] ) == False ):
			error = {"error": "Invalid phone number, make sure phone number is in form of: 	XXX-XXX-XXXX"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		
		# else successfull
		new_user = User.create_new_user(post_data["username"],
						post_data["password"],
						post_data["zip_code"],
						post_data["email"],
						post_data["phone_number"],
						post_data["default_pickup_arrangements"])
		return_user = { "id": new_user.id,
				"username": new_user.username,
				"zip_code": new_user.zip_code,
				"email": new_user.email,
				"phone_number": new_user.phone_number,
				"default_pickup_arrangements": new_user.default_pickup_arrangements,
				"is_shed_coordinator": new_user.is_shed_coordinator,
				"is_admin": new_user.is_admin }
		request.session['user'] = return_user
		return HttpResponse(json.dumps(return_user), content_type="application/json")
	"""
		password mismatch
		invalid zipcode
		invalid email
		invalid phone number
		user is shed coorinator can't change zipcode
		user has tools loaned out, can't change zip
		user is borrowing tools, can't change zip
	"""
	if request.method == 'PUT':
		put_data = json.loads(request.body.decode("utf-8"))

		# invalid zipcode -- error 400
		if len(put_data["zip_code"]) != 5:
			error = {"error": "invalid zip code! (wrong len)"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		try:
			is_int = int(put_data["zip_code"])
		except ValueError:
			error = {"error": "invalid zip code! (not an int)"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		
		# invalid email -- error 400
		try:
			validate_email( put_data["email"] )
		except ValidationError:
			error = {"error": "You entered an invalid email address!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# invalid phone number -- error 400
		if validate_phone_number(put_data["phone_number"]) == False:
			error = {"error": "invalid phone number, make sure phone number is in form of: XXX-XXX-XXXX!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# user is shed coordinator, can't change zip -- error 403
		if request.session['user']['is_shed_coordinator']:
			error = {"error": "You are currently shed coordinator, you may not change your zip code.  Please contact admin."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=403)

		# user has tools being borrowed, can't change zip -- error 403

		# user is borrowing tools, can't change zip -- error 403

		update_user = User.update_user( request.session['user']['username'],
						put_data['phone_number'],
						put_data['zip_code'],
						put_data['email'],
						put_data['default_pickup_arrangements'])
		return_user = {	"id": update_user.id,
				"username": update_user.username,
				"zip_code": update_user.zip_code,
				"email": update_user.email,
				"phone_number": update_user.phone_number,
				"default_pickup_arrangements": update_user.default_pickup_arrangements,
				"is_shed_coordinator": update_user.is_shed_coordinator,
				"is_admin": update_user.is_admin} 
		request.session["user"] = return_user
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
		# username does not exist
		if User.get_user_by_username(post_data["username"]) == False:
			error = {"error": "Username does not exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		
		# password is incorrect
		user = User.get_user_by_username(post_data["username"])
		if post_data["password"] != user.password:
			error = {"error": "Invalid password"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		user = User.get_user_by_username(post_data['username'])
		return_user = {"id": user.id, 
				"username" : user.username, 
				"zip_code": user.zip_code, 
				"email": user.email, 
				"phone_number": user.phone_number, 
				"default_pickup_arrangements": user.default_pickup_arrangements, 
				"is_shed_coordinator": user.is_shed_coordinator, 
				"is_admin":user.is_admin}
		request.session['user'] = return_user
		return HttpResponse(json.dumps(return_user), content_type="application/json")

def validate_phone_number( phone_number ):
	if( len(phone_number) != 12 ):
		return False
	for i in range(12):
		if i in [3, 7]:
			if( phone_number[i] != '-' ):
				return False
		else:
			try:
				is_int = int(phone_number[i])
			except ValueError:
				return False
	return True

@csrf_exempt
def changePassword(request):
	"""
	If passwords don't match
	Old password is wrong
	Invalid password
	"""
	if request.method == "PUT":
		put_data = json.loads(request.body.decode("utf-8"))
		userID = request.session['user']['id']
		user = User.get_user(userID)
		return_message = {}
		if (user.password==put_data['old_password']):
			if (put_data['new_password'] == put_data['confirm_new_password']):
				user.update_password(userID, put_data['new_password'])
				return_message = {"id": user.id, 
						"username" : user.username, 
						"zip_code": user.zip_code, 
						"email": user.email, 
						"phone_number": user.phone_number, 
						"default_pickup_arrangements": user.default_pickup_arrangements, 
						"is_shed_coordinator": user.is_shed_coordinator, 
						"is_admin":user.is_admin}
						
			else:
				return_message = {"error":"mismatch passwords"}
				#return_message = ERROR
		else:
			return_message = {"error":"incorrect old password"}
			#return_message = ERROR
		return HttpResponse(json.dumps(return_message), content_type="application/json")

@csrf_exempt
def logout(request):
	if request.method == "DELETE":
		request.session.flush()
#		print(request.session["user"])
		return_message = {"message": "Logout successful!"}
		return HttpResponse(json.dumps(return_message), content_type="application/json")
