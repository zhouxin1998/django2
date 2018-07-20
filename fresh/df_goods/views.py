# coding=utf-8
from django.shortcuts import render
from models import TypeInfo,GoodsInfo
from django.core.paginator import Paginator
from df_cart.models import *
# Create your views here.
def index(request):
    typelist = TypeInfo.objects.all()
    # 最新的四条
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    # 点击量最多的四条
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]

    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]

    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]

    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]

    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]

    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]


    context = {
        'title':'首页','cat_page':1,
        'type0':type0,'type01':type01,
        'type1':type1,'type11':type11,
        'type2':type2,'type21':type21,
        'type3':type3,'type31':type31,
        'type4':type4,'type41':type41,
        'type5':type5,'type51':type51,
        'cart_count':cart_count(request),
    }
    return render(request,'df_goods/index.html',context)

def list(request,tid,pindex,sort):
    # tid,pindex,sort 分类id,分页索引,排序
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')
    if sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-gprice')
    if sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-gclick')

    pageinator = Paginator(goods_list,10)
    page = pageinator.page(int(pindex))
    context = {
        'title': '列表',
        'news':news,'cat_page':1,
        'goods_list':goods_list,
        'typeinfo':typeinfo,
        'pageinator':pageinator,
        'page':page,
        'sort':sort,
        'cart_count':cart_count(request),
    }
    return render(request,'df_goods/list.html',context)

def detail(request,id):
    # goods = GoodsInfo.objects.get(pk=int(id))

    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick = goods.gclick + 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': '详情',
        'cat_page': 1,
        'news': news,
        'goods': goods,
        'cart_count':cart_count(request),
    }

    response = render(request, 'df_goods/detail.html', context)
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d'%goods.id
    if goods_ids != '':#有goods_id
        goods_ids1 = goods_ids.split(',')#拆分成列表
        if goods_ids1.count(goods_id) >=1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)
        if len(goods_ids1)>5:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)

    else:#没有goods_id　保存到goods_ids
        goods_ids = goods_id
    response.set_cookie('goods_ids',goods_ids)

    return response

# 购物车数量
def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0


# 全文检索
from haystack.views import SearchView

class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title']= '搜索'
        context['cat_page']=1
        context['cart_count']=cart_count(self.request)
        return context


