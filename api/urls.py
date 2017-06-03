from django.conf.urls import url
from django.contrib import admin
from api import views
urlpatterns = [
url(r'^stock/$',  views.stock),
    # url(r'^$/stock', views.stock),
    # url(r'^$/company', 'api.views.company'),
]