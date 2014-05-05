from django.conf.urls import patterns, include, url
from .api_routes import borrowTransaction, getToolsBorrowing, getToolsLending, resolve_borrow_request, resolve_end_borrow_request, get_unresolved_borrow_transactions, get_rejected_requests, get_end_borrow_transaction_requests, get_all_return_pending_bt_in_community_shed, pull_entire_community
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
		url(r'^api/borrowTransaction$', borrowTransaction),
		url(r'^api/borrowTransaction/borrowing/(?P<user_id>\w{0,50})$', getToolsBorrowing),
		url(r'^api/borrowTransaction/borrowed/(?P<user_id>\w{0,50})$', getToolsLending),
		url(r'^api/borrowTransaction/resolve$', resolve_borrow_request),
		url(r'^api/borrowTransaction/requestPending$', get_unresolved_borrow_transactions),
		url(r'^api/borrowTransaction/endRequests$', get_end_borrow_transaction_requests),
		url(r'^api/borrowTransactions/pendingCommunity$', get_all_return_pending_bt_in_community_shed),
		url(r'^api/borrowTransaction/(?P<bt_id>\w{0,50})$', resolve_end_borrow_request),
		url(r'^api/borrowTransaction/rejected/(?P<user_id>\w{0,50})$', get_rejected_requests),
		url(r'^api/borrowTransactions/community/(?P<zip_code>\w{0,50})$', pull_entire_community),
#		url(r'^api/borrowTransaction/endRequests$', get_end_borrow_transaction_requests),
#		url(r'^api/borrowTransaction/requestPending$', get_unresolved_borrow_transactions),
)
