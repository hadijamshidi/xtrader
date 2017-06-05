from django.conf.urls import url
from django.contrib import admin
from api import views

urlpatterns = [
    url(r'^stock/$', views.stock),
    url(r'^history/$', views.history),
    url(r'^update/history/$', views.update_history),
    # url(r'^$/company', 'api.views.company'),
]
