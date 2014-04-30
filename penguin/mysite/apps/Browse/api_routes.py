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
from ..Tools.api_routes import tool_to_json

"""
Takes a BorrowTransaction object and converts it into a dictionary for use with json

@param transaction  the borrow transaction object

@return  python dictionary 
"""
def bt_to_json(transaction):
	return_tool= tool_to_json(transaction.tool)
	return_bt = {	"id": transaction.id,
			"tool": return_tool,
			"status": transaction.status,
			"borrower_message": transaction.borrower_message,
			"owner_message": transaction.owner_message,
			"borrower": transaction.borrower.username,
			"due_date": dt_to_milliseconds(transaction.tool.available_date) }
	return return_bt
			

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
		borrow_transaction = BorrowTransaction.create_new_borrow_transaction(user, current_tool, post_data["borrower_message"])
		return_bt = bt_to_json(borrow_transaction)
		return HttpResponse(json.dumps(return_bt), content_type="application/json")
		
	"""
		BT PUT (end a borrow transaction)
		Owner doesn't accept return
		Tool doesn't exist
	"""

#	if request.method == "PUT":
#		post_data = json.loads(request.body.decode("utf-8"))
#		
#		#Make sure tool exists
#		try:
#			current_tool = Tool.get_tool(post_data['toolId'])
#		except:
#			return HttpResponse(json.dumps({"error":"Invalid tool"}), content_type="application/json", status=400)
#		
#		transaction = BorrowTransaction.get_current_borrow_transaction_by_tool(post_data['toolId'])
#		BorrowTransaction.end_borrow_transaction(transaction.id)
#		#return_bt = {"id": bt.id, "toolId": post_data['toolId'], "borrowerId": bt.borrower.id}
#		return_bt = bt_to_json(transaction)
#		return HttpResponse(json.dumps(return_bt), content_type="application/json")

	"""
	PUT
	api_route -> request to end borrow transaction
	"""
	if request.method == "PUT":
		put_data = json.loads(request.body.decode("utf-8"))
		bt = BorrowTransaction.get_current_borrow_transaction_by_tool(put_data["toolId"])
		transaction = BorrowTransaction.request_end_borrow_transaction(bt.id)
		return_bt = bt_to_json(transaction)
		return HttpResponse(json.dumps(return_bt), content_type="application/json")
		
@csrf_exempt
def getToolsBorrowing(request, user_id):
	if request.method == "GET":
		transactions = BorrowTransaction.get_borrower_borrow_transactions(user_id)
		return_tools = []
		for transaction in transactions:
			return_tools.append(tool_to_json(transaction.tool))
				
		return HttpResponse(json.dumps(return_tools), content_type="application/json")
		
		
@csrf_exempt
def getToolsLending(request, user_id):
	if request.method == "GET":
		tools_lending = []
		transactions = BorrowTransaction.get_borrow_transaction_user_owns(user_id)
		for transaction in transactions:
				tools_lending.append(tool_to_json(transaction.tool))
				
		return HttpResponse(json.dumps(tools_lending), content_type="application/json")

@csrf_exempt
def resolve_borrow_request(request):
	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		if post_data["resolution"] == "True":
			bt = BorrowTransaction.get_request_pending_borrow_transaction_by_tool(post_data["toolId"])
			approved_bt = BorrowTransaction.approve_borrow_transaction(bt.get_borrow_transaction_id())
			return_bt = bt_to_json(approved_bt)
			return HttpResponse(json.dumps(return_bt), content_type="application/json")
		if post_data["resolution"] == "False":
			bt = BorrowTransaction.get_request_pending_borrow_transaction_by_tool(post_data["toolId"])
			rejected_bt = BorrowTransaction.reject_borrow_transaction(bt.get_borrow_transaction_id(), post_data["owner_message"])
			return_bt = bt_to_json(rejected_bt)
			return HttpResponse(json.dumps(return_bt), content_type="application/json")

@csrf_exempt
def resolve_end_borrow_request(request, bt_id):
	if request.method == "DELETE":
		bt = BorrowTransaction.end_borrow_transaction(bt_id)
		return_bt = bt_to_json(bt)
		return HttpResponse(json.dumps(return_bt), content_type="application/json")

"""
GET
url -> /api/borrowTransaction/requestPending
"""
@csrf_exempt
def get_unresolved_borrow_transactions(request): # something funky is going on?
	if request.method == "GET":
		user_id = request.session['user']['id']
		unresolved_transactions = BorrowTransaction.get_unresolved_borrow_transactions(user_id)
		return_transactions = []
		print(unresolved_transactions)
		for transaction in unresolved_transactions:
			return_bt = bt_to_json(transaction)
			return_transactions.append(return_bt)
		return HttpResponse(json.dumps(return_transactions), content_type="application/json")

"""
GET
url -> /api/borrowTransaction/rejected/:id
"""
@csrf_exempt
def get_rejected_requests(request, user_id):
	if request.method == "GET":
		rejected_requests = BorrowTransaction.get_rejected_borrow_transactions(user_id)
		return_transactions = []
		for transaction in rejected_requests:
			return_bt = bt_to_json(transaction)
			return_transactions.append(return_bt)
		return HttpResponse(json.dumps(return_transactions), content_type="application/json")

"""
GET
url -> /api/borrowTransaction/endRequests
"""
@csrf_exempt
def get_end_borrow_transaction_requests(request):
	if request.method == "GET":
		end_requests = BorrowTransaction.get_return_pending_borrow_transactions(request.session['user']['id'])
		return_transactions = []
		for transaction in end_requests:
			return_bt = bt_to_json(transaction)
			return_transactions.append(return_bt)
		return HttpResponse(json.dumps(return_transactions), content_type="application/json")
