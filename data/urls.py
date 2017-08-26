from django.conf.urls import url
from data import views, update

urlpatterns = [
    url(r'^update', update.update_all_data, name='update'),
    url(r'^mabna/$', views.mabnaAPI, name='mabna api'),
    url(r'^history/$', views.history),
    url(r'^stockwatch/(?P<SymbolId>\w+)/$', views.stockwatch),
    url(r'^symbol-search/q=(?P<query>\w+)', views.symbol_search, name='symbol_search'),
    url(r'^get-data/(?P<SymbolId>\w+)/', views.get_data, name='get_data'),
]
