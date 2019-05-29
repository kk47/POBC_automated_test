"""pobc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import home.views as views
import warning.views as warning
import home.login as login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login.login_view),
    path('logout', login.logout_view),


    path('', views.index),


    path('mail/', warning.mail),
    path('mail/data/', warning.mail_data),

    path('rule/', warning.rule),
    path('rule/data/', warning.rule_data),
    path('rule/var/', warning.rule_var),

    path('message/', warning.message),
    path('message/data/', warning.message_data),
    path('message/<mid>/', warning.read_message),

    path('test/', views.test),
]
