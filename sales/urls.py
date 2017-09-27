from django.conf.urls import url
from sales import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    url(r'^payment_callback/$', views.payment_callback),
    url(r'^start/(?P<subscribe_id>\d+)/$', views.start_pay),
]
