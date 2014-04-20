from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.utils import timezone
from .models import BorrowTransaction
from ..Tools.models import Tool
from ..Users.models import User
from ...json_datetime import dt_to_milliseconds, milliseconds_to_dt


@csrf_exempt
def borrowTransaction(request):
	"""
		BT POST (Create new borrow transaction)
		Tool doesn't exist
		Tool currently being borrowed
		Invalid date
	"""
	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		current_tool = None
		
		#Make sure tool exists
		try:
			current_tool = Tool.get_tool(post_data['toolId'])
		except:
			return HttpResponse(json.dumps({"error":"Invalid tool"}), content_type="application/json", status=400)
		
		#check if tool is currently being borrowed
		if not Tool.is_tool_available(post_data['toolId']):
			return HttpResponse(json.dumps({"error":"Tool being borrowed already"}), content_type="application/json", status=400)
		
		milliseconds = int(post_data['date'])
		rent_date = milliseconds_to_dt(milliseconds)
		
		#verify date is allowed
		if (rent_date < datetime.datetime.now()):
			return HttpResponse(json.dumps({"error":"Invalid date"}), content_type="application/json", status=400)
			
		
		Tool.set_tool_unavailable(current_tool.id, rent_date)
		user = User.get_user(request.session['user']['id'])
		borrow_transaction_id = BorrowTransaction.create_new_borrow_transaction(user, current_tool)
		return HttpResponse(json.dumps({"id": borrow_transaction_id, "toolId": current_tool.id, "borrowerId": user.id, "date": milliseconds}), content_type="application/json")
		
	"""
		BT PUT (end a borrow transaction)
		Owner doesn't accept return
		Tool doesn't exist
	"""
	if request.method == "PUT":
		post_data = json.loads(request.body.decode("utf-8"))
		#Make sure tool exists
		try:
			current_tool = Tool.get_tool(post_data['toolId'])
		except:
			return HttpResponse(json.dumps({"error":"Invalid tool"}), content_type="application/json", status=400)
		bt = BorrowTransaction.get_current_borrow_transaction_by_tool(post_data['toolId'])
		BorrowTransaction.end_borrow_transaction(bt.id)
		return_bt = {"id": bt.id, "toolId": post_data['toolId'], "borrowerId": bt.borrower.id}
		return HttpResponse(json.dumps(return_bt), content_type="application/json")
		
		
@csrf_exempt
def getToolsBorrowing(request, user_id):
	if request.method == "GET":
		transactions = BorrowTransaction.get_borrower_borrow_transactions(user_id)
		return_transactions = []
		for transaction in transactions:
			return_transactions.append({"id": transaction.id,
				"toolID": transaction.tool.id,
				"borrowerID": transaction.borrower.id,
				"date": dt_to_milliseconds(transaction.tool.available_date)})
				
		return HttpResponse(json.dumps(return_transactions), content_type="application/json")
		
		
@csrf_exempt
def getToolsLending(request, user_id):
	if request.method == "GET":
		tools_lending = []
		bt = BorrowTransaction.get_borrow_transaction_user_owns(user_id)
		for transaction in bt:
				tools_lending.append({"id": user_id,
					"toolID": transaction.tool.id,
					"borrowerID": transaction.borrower.id,
					"date": dt_to_milliseconds(transaction.tool.available_date)})
				
		return HttpResponse(json.dumps(tools_lending), content_type="application/json")
