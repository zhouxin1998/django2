# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from login.models import UserInfo
from df_cart.models import CartInfo
from login import user_decorator
# from django.template import RequestContext, loader
from django.db import transaction
from models import OrderInfo,OrderDetailInfo
from datetime import datetime


# Create your views here.

@user_decorator.login
def df_order(request):
    # red = HttpResponse()
    # 查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 根据提交，查询购物车信息
    if request.method == 'POST':
        get = request.POST
        cart_ids = get.getlist('cart_id')
        cart_ids1 = [int(item) for item in cart_ids]
        request.session['cart_ids1'] = cart_ids1
        request.session['cart_ids'] = cart_ids
        carts = CartInfo.objects.filter(id__in=cart_ids1)
    else:
        cart_ids1 = request.session.get('cart_ids1',default=None)
        cart_ids = request.session.get('cart_ids',default=None)
        # print(cart_ids1)
        carts = CartInfo.objects.filter(id__in=cart_ids1)

    context = {
        'title':'提交订单','user_page':1,
        'user':user,
        'carts':carts,
        'cart_ids':','.join(cart_ids)
    }
    # t1 = loader.get_template('df_order/place_order.html')cart_ids
    # context = RequestContext(request, context)
    # return HttpResponse(t1.render(context))
    return render(request,'df_order/place_order.html',context)

@user_decorator.login
def site1(request):
    # 修改收货地址，返回当前页面
    red = HttpResponseRedirect('/user/site/')
    red.set_cookie('url1', 'tt')
    return red


@transaction.atomic()
@user_decorator.login
def order_handle(request):

    tran_id = transaction.savepoint()
    # 接收购物车编号
    cart_ids = request.POST.get('cart_ids')
    # print(cart_ids)
    try:
        #创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid

        order.odate = now
        order.ototal = 0
        order.save()
        # 创建订单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        total = 0
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order

            #　查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods = cart.goods
            if goods.gkucun >= cart.count:#如果库存大于购买量
                goods.gkucun = cart.goods.gkucun-cart.count
                goods.save()

                print(cart_ids1)
                # 详单信息
                detail.goods_id = goods.id
                price = goods.gprice
                detail.price = price
                count = cart.count
                detail.count = count
                detail.save()
                total = total+price*count
                # 删除购物车数据
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return HttpResponseRedirect('/cart/')
        #保存总价
        order.ototal = total+10
        order.save()

    except Exception:
        print(Exception)
        # print(111111)
        transaction.savepoint_rollback(tran_id)

    return HttpResponseRedirect('/user/user_center/')


@user_decorator.login
def pay(request,oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context = {'order':order}
    return render(request,'df_order/pay.html',context)

