# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from models import UserInfo
from df_goods.models import GoodsInfo
from hashlib import sha1
from df_order.models import OrderInfo
from django.core.paginator import Paginator,Page

import user_decorator

import json
# Create your views here.
def register(request):
    return render(request, 'login/register.html',{'title':'用户注册'})

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

# 用户名是否存在
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

    # 查询数据库用户名是否存在
    users = UserInfo.objects.filter(uname=username)

    if len(users) == 1:
        # sha1加密
        sh = sha1()
        sh.update(pwd.encode('utf-8'))
        upwd2 = sh.hexdigest()

        if users[0].upassword == upwd2:
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)#'/user/info'
            # 成功后删除转向地址，防止以后直接登录造成的转向
            red.set_cookie('url','',max_age=-1)
            # 记住用户名
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

# 退出
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')

@user_decorator.login
def user_info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    uname = request.session['uname']
    # 最近浏览
    goods_list = []
    goods_ids = request.COOKIES.get('goods_ids', '')
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')  # ['']
        # GoodsInfo.objects.filter(id__in=goods_ids1)
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'title':'用户中心','uname':uname,'user_email':user_email,'user_page':1,'goods_list':goods_list}
    return render(request,'login/user_center_info.html',context)

@user_decorator.login
def user_order(request,pindex):
    uid =  request.session['user_id']
    order_list = OrderInfo.objects.filter(user_id=uid).order_by('-oid')

    paginator = Paginator(order_list,2)
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))

    context = {
        'title':'用户中心','user_page':1,
        'page_name':1,
        'paginator':paginator,
        'page':page,
    }
    return render(request,'login/user_center_order.html',context)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])

    context = {'title':'用户中心','user':user,'user_page':1}
    return render(request,'login/user_center_site.html',context)

@user_decorator.login
def site_handle(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        uname = post.get('uname')
        uaddress = post.get('uaddress')
        uyoubian = post.get('uyoubian')
        uphone = post.get('uphone')

        user.ushou = uname
        user.uaddress = uaddress
        user.uyoubian = uyoubian
        user.uphone = uphone
        user.save()

        # request.session.flush()
        url = request.session.get('url1',default=None)
        if url == 'tt':
            # request.session['url1'] = None
            del request.session['url1']
            # request.session.clear()
            # request.session.flush()
            red = HttpResponseRedirect('/df_order/')
            return red
    context = {'title': '用户中心', 'user': user, 'user_page': 1}
    return render(request, 'login/user_center_site.html', context)
