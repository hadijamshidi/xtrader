from django.conf.urls import url
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^stock/$', views.stock),
    url(r'^history/$', views.history),
    url(r'^marketwatch/$', views.marketwatch),
    url(r'^start/$', views.update_MarketWatch),
]
