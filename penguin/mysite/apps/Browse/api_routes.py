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
		current_tool = Tool.get_tool(post_data['toolId'])
		milliseconds = int(post_data['date'])
		rent_date = milliseconds_to_dt(milliseconds)
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
		bt = BorrowTransaction.get_current_borrow_transaction_by_tool(post_data['toolId'])
		BorrowTransaction.end_borrow_transaction(bt.id)
		return_bt = {"id": bt.id, "toolId": post_data['toolId'], "borrowerId": bt.borrower.id}
		return HttpResponse(json.dumps(return_bt), content_type="application/json")