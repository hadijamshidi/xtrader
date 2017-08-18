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
    url(r'^farabi', views.farabi, name='farabi'),
    url(r'^.well-known/acme-challenge/_4__Dydo_r-Odxp9vmfg6O0yztz4wubxg1pI_hjN61w', views.ssl, name='ssl'),
    url(r'^trade', views.trade, name='trade'),
    url(r'^portfo', views.portfo, name='portfo'),
    url(r'^orders', views.orders, name='orders'),
    url(r'^edit', views.editOrder, name='edit'),
    url(r'^cancelOrder', views.cancelOrder, name='cancelOrder'),
    url(r'^statusaccount', views.account_status, name='status'),

]
