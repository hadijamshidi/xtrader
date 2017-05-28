from django.conf.urls import url

from . import views
urlpatterns = [

    url(r'^$', views.my_programs),
    # url(r'^registration/(?P<registration_id>\d+)/', 'program.views.registration'),

]
