"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^.well-known/acme-challenge/ODxZzdF8g1qVVcaBy7TTYI9PwVWD_65sFjIlPpDq2Oo', views.ssl,),
    url(r'^$', views.index, name='index'),
    url(r'^symbol-search/q=(?P<query>\w+)', views.symbol_search, name='symbol_search'),
    url(r'^get-data/name=(?P<name>\w+)/', views.get_data, name='get_data'),
    url(r'^indicators-api', views.indicators_api, name='indicatoss_api'),
    url(r'^backtest', views.display, name='display'),
    url(r'^back-test', views.back_test, name='back_test'),
    url(r'^about-us', views.about_us, name='about_us'),
    url(r'^stockwatch/SymbolId=(?P<SymbolId>\w+)', views.stockwatch, name='stockwatch'),

]
