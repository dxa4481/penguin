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

		# date out of range -- status 400
		if milliseconds >= 253370764800000:
			error = {"error": "cannot reserve tool past Dec, 31 9998"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		rent_date = milliseconds_to_dt(milliseconds)
		
		#verify date is allowed
		if (rent_date < datetime.datetime.now()):
			return HttpResponse(json.dumps({"error":"Invalid date"}), content_type="application/json", status=400)
		
		user = User.get_user(request.session['user']['id'])
		borrow_transaction = BorrowTransaction.create_new_borrow_transaction(user, current_tool, post_data["borrower_message"], rent_date)
		return_bt = bt_to_json(borrow_transaction)
		return HttpResponse(json.dumps(return_bt), content_type="application/json")
		
	"""
	PUT
	api_route -> request to end borrow transaction

	possible errors:
	tool does not exist
	transaction does not exist
	"""
	if request.method == "PUT":
		put_data = json.loads(request.body.decode("utf-8"))

		# tool does not exist -- status 400
		try:
			current_tool = Tool.get_tool(put_data["toolId"])
		except:
			error = {"error": "tool does not exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# transaction does not exist -- status 400
		try:
			bt = BorrowTransaction.get_current_borrow_transaction_by_tool(put_data["toolId"])
		except:
			error = {"error": "Transaction does not exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		transaction = BorrowTransaction.request_end_borrow_transaction(bt.id)
		return_bt = bt_to_json(transaction)
		return HttpResponse(json.dumps(return_bt), content_type="application/json")
		
@csrf_exempt
def getToolsBorrowing(request, user_id):
	if request.method == "GET":
		transactions = BorrowTransaction.get_borrower_borrow_transactions(user_id)
		return_tools = []
		for transaction in transactions:
			return_tools.append(bt_to_json(transaction))
				
		return HttpResponse(json.dumps(return_tools), content_type="application/json")
		
		
@csrf_exempt
def getToolsLending(request, user_id):
	if request.method == "GET":
		tools_lending = []
		transactions = BorrowTransaction.get_borrow_transaction_user_owns(user_id)
		for transaction in transactions:
				tools_lending.append(bt_to_json(transaction))
				
		return HttpResponse(json.dumps(tools_lending), content_type="application/json")

"""
POST
url -> /api/borrowTransaction/resolve

possible errors:
tool does not exist
transaction does not exist
tool already approved
resolution not True or False
owner doesn't give message if rejects request
"""
@csrf_exempt
def resolve_borrow_request(request):
	if request.method == "POST":
		post_data = json.loads(request.body.decode("utf-8"))
		
		# tool does not exist -- status 400
		try:
			current_tool = Tool.get_tool(post_data["toolId"])
		except:
			error = {"error": "tool does not exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# transaction does not exist -- status 400
		try:
			bt = BorrowTransaction.get_request_pending_borrow_transaction_by_tool(current_tool.id)
		except:
			error = {"error": "transaction does not exist or has already been approved"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

		# accept borrow request
		if post_data["resolution"]:
			approved_bt = BorrowTransaction.approve_borrow_transaction(bt.get_borrow_transaction_id())
			return_bt = bt_to_json(approved_bt)
			return HttpResponse(json.dumps(return_bt), content_type="application/json")

		# reject borrow request
		if not post_data["resolution"]:
			# owner doesn't give message when rejecting request -- status 400
			if not post_data["owner_message"]:
				error = {"error": "you must provide a message when rejecting a borrow request"}
				return HttpResponse(json.dumps(error), content_type="application/json", status=400)

			rejected_bt = BorrowTransaction.reject_borrow_transaction(bt.get_borrow_transaction_id(), post_data["owner_message"])
			return_bt = bt_to_json(rejected_bt)
			return HttpResponse(json.dumps(return_bt), content_type="application/json")

"""
DELETE
url -> /api/borrowTransaction/:transactionId

possible errors:
transaction does not exist
status is not borrow_return_pending
"""
@csrf_exempt
def resolve_end_borrow_request(request, bt_id):
	if request.method == "DELETE":
		# transaction does not exist -- status 400
		try:
			current_transaction = BorrowTransaction.get_borrow_transaction(bt_id)
		except:
			error = {"error" "transaction does not exist"}

		# transaction status is not borrow_return_pending -- status 400
		if current_transaction.status != "borrow return pending":
			error = {"error": "transaction is not return pending, cannot resolve transaction."}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)
		bt = BorrowTransaction.end_borrow_transaction(bt_id)
		return_bt = bt_to_json(bt)
		return HttpResponse(json.dumps(return_bt), content_type="application/json")

"""
GET
url -> /api/borrowTransaction/requestPending
"""
@csrf_exempt
def get_unresolved_borrow_transactions(request):
	if request.method == "GET":
		user_id = request.session['user']['id']
		unresolved_transactions = BorrowTransaction.get_unresolved_borrow_transactions(user_id)
		return_transactions = []
		for transaction in unresolved_transactions:
			return_bt = bt_to_json(transaction)
			return_transactions.append(return_bt)
		return HttpResponse(json.dumps(return_transactions), content_type="application/json")

"""
GET
url -> /api/borrowTransaction/rejected/:id

possible errors:
user does not exist
"""
@csrf_exempt
def get_rejected_requests(request, user_id):
	if request.method == "GET":
		# user does not exist -- status 400
		try:
			current_user = User.get_user(user_id)
		except:
			error = {"error": "invalid user id, user does not exist"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=400)

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
			if(not transaction.tool.in_community_shed):
				return_bt = bt_to_json(transaction)
				return_transactions.append(return_bt)
		return HttpResponse(json.dumps(return_transactions), content_type="application/json")

"""
GET
url -> /api/borrowTransaction/pendingCommunity

possible errors:
user trying to access this is not a shed coordinator
"""
@csrf_exempt
def get_all_return_pending_bt_in_community_shed(request):
	if request.method == "GET":
		shed_coord = User.get_user_by_username(request.session['user']['username'])

		# user is not shed coordinator -- status 403
		if not shed_coord.is_shed_coordinator:
			error = {"error": "Access denied, you are not the shed coordinator"}
			return HttpResponse(json.dumps(error), content_type="application/json", status=403)

		community_transactions = BorrowTransaction.get_all_return_pending_in_community_shed(shed_coord.zip_code)
		return_transactions = []
		for transaction in community_transactions:
			return_bt = bt_to_json(transaction)
			return_transactions.append(return_bt)
		return HttpResponse(json.dumps(return_transactions), content_type="application/json")
