# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from login import user_decorator
from models import CartInfo
from df_goods.views import cart_count
# Create your views here.

@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title':'购物车',
        'cat_page':1,
        'carts':carts,
        'cart_count': cart_count(request),
    }
    return render(request,'df_cart/cart.html',context)


@user_decorator.login
def add(request,gid,count):
    # 用户购买商品id,数量
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    #查询购物车是否有该商品
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)

    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count+count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'cart_id':cart.id,'count':count})
    else:
        return HttpResponseRedirect('/cart/')

@user_decorator.login
def edit(request,cart_id,count):
    count1 = 1
    cart_id = int(cart_id)
    count = int(count)
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        count1 = cart.count
        cart.count = count
        cart.save()
        data = {'ok':0}
    except Exception:
        data = {'ok':count1}
    return JsonResponse(data)


@user_decorator.login
def delete(request,cart_id):#删除
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok':1}
    except:
        data = {'ok': 0}
    return JsonResponse(data)





