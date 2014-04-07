from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from .models import User
from ...json_datetime import dthandler
