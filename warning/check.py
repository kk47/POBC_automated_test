import importlib
import json
from warning.sendmail import Email
from warning.models import Rule, Mail, Message

def warning(module):
    for row in Rule.objects.filter(module=module):
        graph = importlib.import_module('graph.script.' + row.module)
        filter = json.loads(row.filter)
        if filter:
            page = graph.graph_page(filter)
        else:
            page = graph.graph_page()
        current_value = check(row, page)
        if current_value is not None:
            sendmail(row, current_value)



def check(row, page):
    for chart in page:
        if_has_title = chart.options.get('title') and chart.options['title'][0].get('text')
        if if_has_title and chart.options['title'][0]['text'] == row.chart:
            for series in chart.options['series']:
                if series.get('name') == row.variable:
                    current_value = str(list(series['data'])[-1])
                    if current_value == 'nan':
                        return 'nan'
                    elif eval(current_value + row.condition + row.threshold):
                        return current_value
                    else:
                        return
    print('invalied rule')

def sendmail(row, current_value):
    emails = Mail.objects.filter(id__in=json.loads(row.to))
    email_send = Email(list(map(lambda x: x.email, emails)))
    msg = '您监控的图表"' + row.chart + '"的变量"' + row.variable + '"的当前值为' + current_value + ', 超过您设定的阈值' + row.threshold + '。'
    msg_db = Message(rule_id=row.id, msg=msg, isread=False)
    msg_db.save()
    mail_str = msg + '详情请访问: http://localhost:8000/message/' + str(msg_db.id) + '/'
    email_send.send(mail_str)