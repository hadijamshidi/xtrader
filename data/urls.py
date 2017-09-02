from django.conf.urls import url
from data import views

urlpatterns = [
    url(r'^add', views.add_new_symbol, name='add'),
    url(r'^update', views.update, name='update'),
    url(r'^mabna/$', views.mabnaAPI, name='mabna api'),
    url(r'^history/$', views.history),
    url(r'^stockwatch/(?P<SymbolId>\w+)/$', views.stockwatch),
    url(r'^symbol-search/q=(?P<query>\w+)', views.symbol_search, name='symbol_search'),
    url(r'^get-data/(?P<SymbolId>\w+)/', views.get_data, name='get_data'),
]
