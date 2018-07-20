from django.conf.urls import url
import views

urlpatterns = [
    url(r'^df_order/$', views.df_order),
    url(r'^user/site1/$', views.site1),
    url(r'^order/order_handle/$', views.order_handle),
    url(r'^pay(\d+)/$', views.pay),
]