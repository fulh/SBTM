"""pyecharts_django_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
#-*-coding:utf-8 -*-，
from django.conf.urls import url
from django.urls import path
from charts import views

urlpatterns = [
    path(r'bar/<str:moduleid>', views.ChartView.as_view(), name='demo'),
    url(r'^index/$', views.IndexView.as_view(), name='demo'),
    url(r'^zhengbang/$', views.zhengbagn.as_view(), name='demo'),
    url(r'^progress/$', views.progress.as_view(), name='demo'),
    path(r'Cultivates/<str:moduleid>', views.CultivatesView.as_view(), name='demo'),
    # path(r'info/', views.ModuleView.as_view()),
    path(r'sumdate/', views.ModuleView.as_view()),
    path(r'test/', views.ModuleTestView.as_view()),
    # path(r'liquid/', views.LiquidView.as_view()),
]