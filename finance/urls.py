from django.conf.urls import url
from finance import views

urlpatterns = [
    url(r'^calculate_filter', views.calculate_indicators, name='mabna api'),
    url(r'^save_strategy', views.save_strategy, name='save strategy'),
]
