from django.conf.urls import url
from finance import views

urlpatterns = [
    url(r'^calculate_filter', views.calculate_indicators, name='mabna api'),
    url(r'^save_strategy', views.save_strategy, name='save strategy'),
    url(r'^get_strategy_names', views.get_strategy_names, name='get strategy names'),
    url(r'^load_strategy', views.load_strategy, name='load strategy'),
    url(r'^scan_market', views.scan_market, name='scan market'),
    url(r'^update-indicators', views.update_indicators, name='update_indicators'),
    url(r'^marketwatch', views.market_watch, name='marketwatch'),
    url(r'^filtermarket', views.filtermarket, name='filtermarket'),
    url(r'^indicators-api', views.indicators_api, name='indicatoss_api'),
    url(r'^backtest', views.display, name='backtest'),
    url(r'^back-test', views.back_test, name='back_test'),
    url(r'^about-us', views.about_us, name='about_us'),
    url(r'^$', views.index, name='index'),
    url(r'^stockwatch/(?:(?P<SymbolId>\w+)/)?$',  views.stockwatch, name='stockwatch'),

]
