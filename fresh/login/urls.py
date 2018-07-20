from django.conf.urls import url

import views

urlpatterns = [
    url(r'^user/register/$', views.register),
    url(r'^user/re_user/$', views.re_user),
    url(r'^user/register_exist/$', views.register_exist),
    url(r'^user/login/$', views.login),
    url(r'^user/login_handle/$', views.login_handle),
    url(r'^user/info/$', views.user_info),
    url(r'^user/user_center(\d*)/$', views.user_order),
    url(r'^user/site/$', views.site),
    url(r'^user/logout/$', views.logout),
    url(r'^user/site_handle/$', views.site_handle),


]