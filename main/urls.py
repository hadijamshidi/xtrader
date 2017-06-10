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
    # url(r'^item/name=(?P<name>\w+)/', views.item_detail, name='item_details'),
    url(r'^symbol-search/q=(?P<query>\w+)', views.symbol_search, name='symbol_search'),
    url(r'^get-data/name=(?P<name>\w+)/', views.get_data, name='get_data'),
    url(r'^indicators-api', views.indicators_api, name='indicatoss_api'),


    # TODO: handle this lines later
    # url(r'^$', views.index, name='index'),
    url(r'^$', views.display, name='display'),
    # TODO: finish

    # url(r'^backtest/stock=(?P<stock_name>\w+)', views.display_item, name='display_item'),
    # url(r'^backtest', views.display, name='display'),

    # url(r'^calculate-indicators', views.calculate_indicators, name='calculate_indicators'),
    # url(r'^update-indicators', views.update_indicators, name='update_indicators'),
    # url(r'^amir', views.amir, name='amir'),
    url(r'^back-test', views.back_test, name='back_test'),

    # url(r'^main/', views.main, name='main'),
    # url(r'^favicon.ico', views.favicon, name='favicon'),

    url(r'^about-us', views.about_us, name='about_us'),
    # url(r'^contact-us', views.contact_us, name='contact_us'),

    # url(r'^test', views.test, name='test'),
    # url(r'^base', views.base, name='base'),

    # url(r'^login', views.login, name='login'),
    # url(r'^sign-up', views.signup, name='sign_up'),
]
