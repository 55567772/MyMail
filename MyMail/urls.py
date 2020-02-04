"""MyMail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path, include, re_path
from Urls import get_Template, get_JSON

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', get_Template.main),
    # 获取JSON信息
    re_path(r'JSON/(?P<key>[a-z]{0,2})$', get_JSON.redirect, name='JSON'),
    # 模板调用
    re_path(r'get_tpl/(?P<page_name>[\w.]{0,30})$', get_Template.redirect, name='get_tpl_mo'),
    #
    # # 微信登录页面userinfo
    # path('userinfo', views.userinfo),
    #
    # # 微信JS SDK 接口调用
    # path('wxjssdk/', views.wxjssdk),
    # path('get_signature', views.jsapi_signature),
    # path('log', views.log),
]
