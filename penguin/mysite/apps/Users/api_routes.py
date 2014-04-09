from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json 
import datetime
from .models import User
from ...json_datetime import dthandler



@csrf_exempt
def user(request):
	if request.method == 'GET':
		return HttpResponse(json.dumps({"test": "this is a test", "test_date": datetime.datetime.now()}, default=dthandler), content_type="application/json")
	if request.method == 'POST':
		new_user={"username": request.POST.get('username'),
		"password": request.POST.get('password'),
		"date": datetime.datetime.now()}
		return HttpResponse(json.dumps(new_user, default=dthandler), content_type="application/json")


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
		request.session.user = return_user
		return HttpResponse(json.dumps(return_user, default=dthandler), content_type="application/json")