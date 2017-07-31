from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),to ----->finance
    # url(r'^symbol-search/q=(?P<query>\w+)', views.symbol_search, name='symbol_search'),to ----> data
    # url(r'^get-data/(?P<SymbolId>\w+)/', views.get_data, name='get_data'),to ----> data
    # url(r'^indicators-api', views.indicators_api, name='indicatoss_api'),to ----->finance
    # url(r'^backtest', views.display, name='display'), to ----->finance
    # url(r'^back-test', views.back_test, name='back_test'),to ----->finance
    # url(r'^about-us', views.about_us, name='about_us'),to ----->finance
	# url(r'^stockwatch/(?:(?P<SymbolId>\w+)/)?$',  views.stockwatch, name='stockwatch'),
]
