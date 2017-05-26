from django.conf.urls import url
from mabna import views
urlpatterns = [
	url(r'^api/$',views.get,name='mabna api'),
	]
