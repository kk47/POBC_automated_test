from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from warning.models import Mail, Rule, Message
from datetime import datetime
from itertools import chain
import json
import re
import importlib


# @login_required
# def daily(request):
#     context = {}
#     return render(request, 'daily.html', context)

@login_required
def mail(request):
    context = {}
    return render(request, 'mail.html', context)


@login_required
@csrf_exempt
def mail_data(request):
    if request.method == 'GET':
        pass
    else:
        operation_db(request, Mail)
    return HttpResponse(json.dumps(list(Mail.objects.all().values()), cls=DatetimeEncoder))


@login_required
def rule(request):
    context = {'mails': Mail.objects.all()}
    return render(request, 'rule.html', context)


@login_required
@csrf_exempt
def rule_data(request):
    if request.method == 'GET':
        pass
    else:
        operation_db(request, Rule)
    return HttpResponse(json.dumps(list(Rule.objects.all().values()), cls=DatetimeEncoder))


@login_required
@csrf_exempt
def rule_var(request):
    module_name = request.GET.get('module')
    graph = importlib.import_module('graph.script.' + module_name)
    if request.method == 'GET':
        FILTER = getattr(graph, 'FILTER', {})
        return render(request, 'select.html', {'filter': FILTER})
    else:
        if request.POST.dict():
            page = graph.graph_page(request.POST.dict())
        else:
            page = graph.graph_page()
        vars = {}
        for chart in page:
            if chart.options.get('title') and chart.options['title'][0].get('text'):
                vars[chart.options['title'][0]['text']] = list(
                    filter(None, map(lambda x: x.get('name'), chart.options['series'])))

        return HttpResponse(json.dumps(vars))


@login_required
def message(request):
    context = {}
    return render(request, 'message.html', context)


@login_required
@csrf_exempt
def message_data(request):
    if request.method == 'GET':
        pass
    else:
        operation_db(request, Message)
    msgs = list(map(to_dict, Message.objects.all()))
    return HttpResponse(json.dumps(msgs, cls=DatetimeEncoder))


@login_required
def read_message(request, mid):
    msg = Message.objects.get(id=mid)
    msg.isread = True
    msg.save()
    return HttpResponseRedirect('/graph/' + msg.rule.module + '/')

def to_dict(row):
    row.__dict__['level'] = row.rule.level
    row.__dict__['module'] = row.rule.module
    del row.__dict__['_state']
    return row.__dict__

def operation_db(request, db):
    action = request.GET.get('action')
    if action == 'remove':
        eid = int(request.GET.get('eid'))
        db.objects.get(id=eid).delete()
    elif action == 'edit':
        eid = int(request.GET.get('eid'))
        log = db.objects.get(id=eid)
        data = request.POST.dict()
        for k, v in data.items():
            log.__setattr__(k, v)
        log.save()
    elif action == 'add':
        data = request.POST.dict()
        log = db(**data)
        log.save()
    elif action == 'read':
        eid = int(request.GET.get('eid'))
        log = db.objects.get(id=eid)
        log.isread = True
        log.save()


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M')
        return json.JSONEncoder.default(self, obj)
