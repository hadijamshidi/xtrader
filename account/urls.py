"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from . import views
from .forms import MyPasswordResetForm, MyPasswordChangeForm
from django.contrib.auth import views as authviews

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^register', views.register_view, name='register'),
    url(r'^edit/$', views.edit, name='edit'),

    url(r'^account-activation/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', views.account_activation,
        name='account_activation'),

    # change password urls
    url(r'^password-change/$', views.password_change,
        name='password_change'),
    url(r'^password-change/done/$', views.password_change_done, name='password_change_done'),

    # restore password urls
    url(r'^password-reset/$', authviews.password_reset,
        {'post_reset_redirect': 'account:password_reset_done', 'password_reset_form': MyPasswordResetForm},
        name='password_reset'),
    url(r'^password-reset/done/$', authviews.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        authviews.password_reset_confirm, {'post_reset_redirect': 'account:password_reset_complete'},
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', authviews.password_reset_complete,
        name='password_reset_complete'),

]
