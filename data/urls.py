from django.conf.urls import url
from data import views

urlpatterns = [
    url(r'^mabna/$', views.mabnaAPI, name='mabna api'),
    url(r'^stock/$', views.stock),
    url(r'^history/$', views.history),
    url(r'^marketwatch/$', views.marketwatch),
    url(r'^stockwatch/(?P<SymbolId>\w+)/$', views.stockwatch),
    # SymbolId
    # url(r'^start/$', views.update_MarketWatch),
]
