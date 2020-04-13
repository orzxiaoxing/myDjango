from django.shortcuts import render, redirect
from login.models import *
from login.forms import *
import re
from django import forms


def index(request):
    pass
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        # form表达校验
        if login_form.is_valid():
            # 读取username为 ‘username’的表单提交值，并赋予 username变量
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == password:
                    # 如果is_login为True，则用户已登录
                    if request.session.get('is_login', None):
                        message = "用户已登录！"
                    else:
                        # session中存入键值对信息
                        request.session['is_login'] = True
                        request.session['user_id'] = user.id
                        request.session['user_name'] = user.name
                        return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())


def register(request):
    # 如果用户已登录，重定向至登录页
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        # 用户名
        reg_username = request.POST.get("reg_username").strip()
        # 密码
        reg_password = request.POST.get("reg_password").strip()
        # 确认密码
        reg_confirm_password = request.POST.get("reg_confirm_password").strip()
        # 邮箱
        reg_email = request.POST.get("reg_email").strip()
        # 性别
        reg_sex = request.POST.get("reg_sex")
        if reg_password != reg_confirm_password:
            message = "两次密码不同，请重新输入！"
            return render(request, "register.html", locals())
        else:
            same_username = User.objects.filter(name=reg_username)
            if same_username:
                message = "用户名已存在，请重新输入！"
                return render(request, "register.html", locals())
            same_email = User.objects.filter(email=reg_email)
            if same_email:
                message = "邮箱已存在，请重新输入！"
                return render(request, "register.html", locals())
            if re.match('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}', reg_email) == None:
                message = "邮箱格式错误，请重新输入！"
                return render(request, "register.html", locals())

        # 创建用户
        new_user = User()
        new_user.name = reg_username
        new_user.password = reg_password
        new_user.email = reg_email
        new_user.sex = reg_sex
        new_user.save()
        # 注册成功后跳转至登录页
        return redirect("/login/")
    return render(request, 'register.html', locals())


def logout(request):
    # flush会一次性清空session中所有内容，可以使用下面的方法
    request.session.flush()
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")
