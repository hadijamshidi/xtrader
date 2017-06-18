from django.conf.urls import url
from finance import views

urlpatterns = [
    url(r'^calculate_filter', views.calculate_indicators, name='mabna api'),
    url(r'^save_strategy', views.save_strategy, name='save strategy'),
    url(r'^get_strategy_names', views.get_strategy_names, name='get strategy names'),
    url(r'^load_strategy', views.load_strategy, name='load strategy'),
    url(r'^scan_market', views.scan_market, name='scan market'),

]
