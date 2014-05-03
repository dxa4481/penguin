from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json 
import datetime
from .models import User
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt
from django.core.validators import validate_email, MaxLengthValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re
from ..Browse.models import BorrowTransaction

"""
Takes a user object and converts it into json
@param user  User object
@return  json dictionary
"""
def user_to_json(user):
	return_user = { "id": user.id,
			"username": user.username,
			"zip_code": user.zip_code,
			"email": user.email,
			"phone_number": user.phone_number,
			"default_pickup_arrangements": user.default_pickup_arrangements,
			"is_shed_coordinator": user.is_shed_coordinator,
			"is_admin": user.is_admin }
	return return_user

@csrf_exempt
def user(request):
	"""

	"""
	if request.method == 'GET':
		u_id = request.session['user']['id']
		user = User.get_user(u_id)
		return_user = user_to_json(user)
		return HttpResponse(json.dumps(return_user), content_type="application/json")
	"""
		username already exists
		password mismatch
		invalid email
		invalid zipcode
		invalid phone number
		Missing Fields
		first user to zip, auto promote to shed_coordinator
	"""
	if request.method == 'POST':
		post_data = json.loads(request.body.decode("utf-8"))
		
		# if username already exists -- error 409
		if( User.get_user_by_username(post_data["username"]) != False ):
			error = { "error": "Username already exists" }
			return HttpResponse(json.dumps(error), content_type ="application/json", status=409)

		# Leave username field blank -- error 400
		if not post_data["username"]:
			error = {"error": "username field left blank.  Please provide a username."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# if password doesn't match confirm password -- error 400
		if( post_data["password"] != post_data["confirm_password"] ):
			error = {"error": "passwords do not match!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# Leave password field blank -- error 400
		if not post_data["password"]:
			error = {"error": "password field left blank.  Please provide a password."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# if email not a valid email address -- error 400
		try:
			validate_email( post_data["email"] )
		except ValidationError:
			error = {"error": "You entered an invalid email address!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# if zipcode not a valid zipcode -- error 400
		if( not validate_zip_code(post_data["zip_code"])):
			error = {"error": "You entered an invalid zip code!"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# if phone number not a valid phone number -- error 400
		if( not validate_phone_number( post_data["phone_number"] )):
			error = {"error": "Invalid phone number, make sure phone number is in form of: 	XXX-XXX-XXXX"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# no input given for pick-up arrangements -- error 400
		if not post_data["default_pickup_arrangements"]:
			error = {"error": "must specify your default pickup arrangements, cannot leave blank"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		
		# else successfull
		new_user = User.create_new_user(post_data["username"],
						post_data["password"],
						post_data["zip_code"],
						post_data["email"],
						post_data["phone_number"],
						post_data["default_pickup_arrangements"])
		# check if user is first to zip code
		area_users = User.get_user_by_zip_code(post_data["zip_code"])
		if area_users.count() == 1:	# if user first to zip code, promote them to shed coordinator
			user_id = new_user.id
			User.promote_user_to_shed_coordinator(user_id)
			new_user = User.get_user(user_id)
		return_user = user_to_json(new_user)
		request.session['user'] = return_user
		return HttpResponse(json.dumps(return_user), content_type="application/json")

#	if request.method == "PUT":
#
#		# invalid phone number -- error 400
#		if not validate_phone_number(put_data["phone_number"]):
#			error = {"error": "You entered an invalid phone number!"}
#			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
#
#		if request.session['user']['zip_code'] != put_data['zip_code']:
#		# user is shed coordinator, can't change zip -- error 403
#			if request.session["user"]["is_shed_coordinator"]:
#				error = {"error": "You are currently shed coordinator, you may not change your zip code.  Please contact an admin."}
#				return HttpResponse(json.dumps(error), content_type="application/json", status=403)
#
#		# user has tools being borrowed, can't change zip -- error 403
#			current_user = User.get_user_by_username(request.session['user']["username"])
#			if BorrowTransaction.get_unresolved_borrow_transactions(current_user.id):
#				error = {"error": "Some of your tools are currently being borrowed, you may not change your zip code.  Please contact an admin."}
#				return HttpResponse(json.dumps(error), content_type="application/json", status=403)
#
#		# user is borrowing tools, can't change zip -- error 403
#			if BorrowTransaction.get_borrower_borrow_transactions(current_user.id):
#				error = {"error": "You are currently borrowing tools, you may not change your zip code.  Please contact an admin."}
#				return HttpResponse(json.dumps(error), content_type="application/json", status=403)
#
#		# default pickup arrangements field left blank -- error 400
#		if not put_data["default_pickup_arrangements"]:
#			error ={"error": "pickup arrangements field was left blank.  Please specify your pickup arrangements"}
#			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
#
#		update_user = User.update_user( request.session['user']['username'],
#						put_data['phone_number'],
#						put_data['zip_code'],
#						put_data['email'],
#						put_data['default_pickup_arrangements'])
#		return_user = user_to_json(update_user)
#		request.session["user"] = return_user
#		return HttpResponse(json.dumps(return_user), content_type="application/json")

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
		current_user = request.session['user']['id']
		if(user_id == current_user.id or current_user.is_admin==True):
			try:
				User.delete_user(user_id)
				returnmsg = { 'success': True }
			except:
				returnmsg = { 'success': False }
				 
			return HttpResponse(json.dumps(returnmsg), content_type="application/json")
		else:
			error = {"error":"Unauthorized access."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=401)
		
		
	"""
	UPDATE USER
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
		u_id = request.session['user']['id']
		current_user_id = int(u_id)
		user_id = int(user_id)
		current_user = User.get_user(current_user_id)
		if((user_id == current_user_id) or (current_user.is_admin==True)):
			
			# invalid zipcode -- error 400
			if (not validate_zip_code(put_data["zip_code"])):
				error = {"error": "invalid zip code!"}
				return HttpResponse(json.dumps(error), content_type="application/json", status=400)
			
			# invalid email -- error 400
			try:
				validate_email( put_data["email"] )
			except ValidationError:
				error = {"error": "You entered an invalid email address!"}
				return HttpResponse(json.dumps(error), content_type="application/json", status=400)
	
			# invalid phone number -- error 400
			if not validate_phone_number(put_data["phone_number"]):
				error = {"error": "You entered an invalid phone number!"}
				return HttpResponse(json.dumps(error), content_type="application/json", status=400)
	
			if request.session['user']['zip_code'] != put_data['zip_code']:
			# user is shed coordinator, can't change zip -- error 403
				if request.session["user"]["is_shed_coordinator"]:
					error = {"error": "You are currently shed coordinator, you may not change your zip code.  Please contact an admin."}
					return HttpResponse(json.dumps(error), content_type="application/json", status=403)
	
			# user has tools being borrowed, can't change zip -- error 403
				current_user = User.get_user_by_username(request.session['user']["username"])
				if BorrowTransaction.get_borrow_transaction_user_owns(current_user.id):
					error = {"error": "Some of your tools are currently being borrowed, you may not change your zip code.  Please contact an admin."}
					return HttpResponse(json.dumps(error), content_type="application/json", status=403)
	
			# user is borrowing tools, can't change zip -- error 403
				if BorrowTransaction.get_borrower_borrow_transactions(current_user.id):
					error = {"error": "You are currently borrowing tools, you may not change your zip code.  Please contact an admin."}
					return HttpResponse(json.dumps(error), content_type="application/json", status=403)
	
			# default pickup arrangements field left blank -- error 400
			if not put_data["default_pickup_arrangements"]:
				error ={"error": "pickup arrangements field was left blank.  Please specify your pickup arrangements"}
				return HttpResponse(json.dumps(error), content_type="application/json", status=400)
	
			update_user = User.update_user( request.session['user']['username'],
							put_data['phone_number'],
							put_data['zip_code'],
							put_data['email'],
							put_data['default_pickup_arrangements'])
			return_user = user_to_json(update_user)
			request.session["user"] = return_user
			return HttpResponse(json.dumps(return_user), content_type="application/json")
		else:
			error = {"error":"Unauthorized access."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=401)

		
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
		if not user.verify_password(post_data["password"]):
			error = {"error": "Invalid password"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		user = User.get_user_by_username(post_data['username'])
		return_user = user_to_json(user)
		request.session['user'] = return_user
		return HttpResponse(json.dumps(return_user), content_type="application/json")

def validate_phone_number( phone_number ):
	regex_phone_number = re.compile("^[\s()+-]*([0-9][\s()+-]*){6,20}$")
	return regex_phone_number.match(phone_number)
def validate_zip_code(zip_code):
	regex_zip_code = re.compile("(^\d{5}(-\d{4})?$)|(^[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}$)")
	return regex_zip_code.match(zip_code)

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
		if (user.verify_password(put_data['old_password'])):
			if (put_data['new_password'] == put_data['confirm_new_password']):
				user.update_password(userID, put_data['new_password'])
				return_message = user_to_json(user)
						
			else:
				return_message = {"error":"mismatch passwords"}
				return HttpResponse(json.dumps(return_message), content_type="application/json", status=400)
		else:
			return_message = {"error":"incorrect old password"}
			return HttpResponse(json.dumps(return_message), content_type="application/json", status=400)
		return HttpResponse(json.dumps(return_message), content_type="application/json")

@csrf_exempt
def logout(request):
	if request.method == "POST":
		request.session.flush()
		return_message = {"message": "Logout successful!"}
		return HttpResponse(json.dumps(return_message), content_type="application/json")

@csrf_exempt
def get_admins(request):
	if request.method == "GET":
		admins = User.get_all_admins()
		return_list = []
		for admin in admins:
			return_list.append(user_to_json(admin))
		return HttpResponse(json.dumps(return_list), content_type="application/json")

@csrf_exempt
def shedCoord(request):
	if request.method == "PUT":
		if (User.get_user(request.session['user']['id']).is_admin == True):
			
			put_data = json.loads(request.body.decode("utf-8"))
			new_shed_coord = User.get_user(put_data['promote'])
			zip_c = new_shed_coord.zip_code
			
			if (User.does_shed_coord_exist(zip_c)):
				User.demote_user_from_shed_coordinator(User.get_shed_coordinator_for_zip(zip_c).id)
		
			User.promote_user_to_shed_coordinator(new_shed_coord.id)
			
			return_user = user_to_json(User.get_user(new_shed_coord.id))
			return HttpResponse(json.dumps(return_user), content_type="application/json")
		else:
			error = {"error":"Unauthorized access."}
			return HttpResponse(json.dumps(errror), content_type="application/json", status=401)
