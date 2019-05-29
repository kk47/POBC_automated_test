from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from warning.check import warning
import json
import importlib

# @login_required
# def daily(request):
#     context = {}
#     return render(request, 'daily.html', context)


@login_required
def index(request):
    context = {}
    return render(request, 'index.html', context)


@login_required
def test(request):
    context = {}
    return render(request, 'test.html', context)

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M')
        return json.JSONEncoder.default(self, obj)