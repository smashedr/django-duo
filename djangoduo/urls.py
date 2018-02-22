from django.contrib import admin
from django.templatetags.static import static
from django.urls import path
from django.views.generic.base import RedirectView

import auth.views as auth
import home.views as home

urlpatterns = [
    path('favicon\.ico', RedirectView.as_view(
        url=static('images/favicon.ico')
    )),
    path('', home.home_view, name='home_view'),
    path('login/', auth.login_view, name='login_view'),
    path('auth/', auth.do_login, name='do_login'),
    path('duo/', auth.do_duo, name='do_duo'),
    path('logout/', auth.do_logout, name='do_logout'),
    path('admin/', admin.site.urls, name='django_admin'),
]
