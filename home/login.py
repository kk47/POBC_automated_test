from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
import json


def login_view(request):
    if request.method == "GET":
        return render(request, 'login.html')

    username = request.POST['username'].strip()
    password = request.POST['password'].strip()
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            info = {'res': True, 'data': request.GET.get('next', '/')}
            #return HttpResponseRedirect(request.GET.get('next', '/'))
            # Redirect to a success page.
        else:
            info = {'res': False, 'data': '该用户已被禁用'}
            # Return a 'disabled account' error message
    else:
        info = {'res': False, 'data': '用户名或密码错误'}

    return HttpResponse(json.dumps(info))
        

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')