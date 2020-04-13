from django.contrib import admin

from login.models import *
#User表注册到admin控台
admin.site.register(User)
