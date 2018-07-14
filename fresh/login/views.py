# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from models import UserInfo
from hashlib import sha1

import json
# Create your views here.
def register(request):
    return render(request, 'login/register.html',{'erorrval':json.dumps({'erorrval':'提示信息'})})

# 注册
def re_user(request):

    if request.method == 'POST':

        post = request.POST
        uname = post.get('user_name')
        upwd = post.get('pwd')
        upwd2 = post.get('cpwd')
        uemail = post.get('email')

        # sha1加密
        sh = sha1()
        sh.update(upwd2.encode('utf-8'))
        upwd3 = sh.hexdigest()

        if upwd != upwd2:
            return HttpResponseRedirect('/user/register/')
        else:
            userinfo = UserInfo()
            userinfo.uname = uname
            userinfo.upassword = upwd3
            userinfo.uemail = uemail
            userinfo.save()

    return HttpResponseRedirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('name')
    # 查询数据库用户名是否存在，返回数量
    count = UserInfo.objects.filter(uname = uname).count()

    return JsonResponse({'count':count})


# 登录
def login(request):
    username = request.GET.get('uname','')
    context = {'title': '用户登录', 'eroor_name': 1, 'error_pwd': 1, 'uname': username}
    return render(request, 'login/login.html',context)


def login_handle(request):
    # if request.method == 'POST':
    post = request.POST
    username = post.get('username')
    pwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    print(jizhu)
    # 查询数据库用户名是否存在
    users = UserInfo.objects.filter(uname=username)

    if len(users) == 1:
        # sha1加密
        sh = sha1()
        sh.update(pwd.encode('utf-8'))
        upwd2 = sh.hexdigest()

        if users[0].upassword == upwd2:
            red = HttpResponseRedirect('/user/info')
            if jizhu == 'on':
                red.set_cookie('uname',username)
            else:
                red.set_cookie('uname','', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['uname'] = username
            return red
        else:
            context = {'title': '用户登录', 'eroor_name': 1, 'error_pwd': 0, 'uname': username, 'upwd': pwd}
            return render(request, 'login/login.html', context)
    else:
        context = {'title':'用户登录','eroor_name':0,'error_pwd':1,'uname':username,'upwd':pwd}
        return render(request,'login/login.html',context)


def user_info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    uname = request.session['uname']
    context = {'uname':uname,'user_email':user_email}
    return render(request,'login/user_center_info.html',context)

def user_center(request):
    return render(request,'login/user_center_order.html')

def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        uname = post.get('uname')
        uaddress = post.get('uaddress')
        uyoubian = post.get('uyoubian')
        uphone =post.get('uphone')


        user.ushou = uname
        user.uaddress = uaddress
        user.uyoubian = uyoubian
        user.uphone = uphone
        user.save()

    context = {'title':'用户中心','user':user}
    return render(request,'login/user_center_site.html',context)


