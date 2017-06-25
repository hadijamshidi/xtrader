from django.conf.urls import url
from following import views

urlpatterns = [
    url(r'^trader=(?P<trader>\w+)/strategy=(?P<strategy>\w+)/', views.show_trader_strategy, name='show trader strategy'),
]
