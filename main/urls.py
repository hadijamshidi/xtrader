from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^symbol-search/q=(?P<query>\w+)', views.symbol_search, name='symbol_search'),
    url(r'^get-data/(?P<SymbolId>\w+)/', views.get_data, name='get_data'),
    url(r'^indicators-api', views.indicators_api, name='indicatoss_api'),
    url(r'^backtest', views.display, name='display'),
    url(r'^back-test', views.back_test, name='back_test'),
    url(r'^about-us', views.about_us, name='about_us'),
	url(r'^stockwatch/(?:(?P<SymbolId>\w+)/)?$',  views.stockwatch, name='stockwatch'),
]
