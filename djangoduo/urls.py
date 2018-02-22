from django.contrib import admin
from django.templatetags.static import static
from django.urls import path
from django.views.generic.base import RedirectView

import login.views as login
import home.views as home

urlpatterns = [
    path('favicon\.ico', RedirectView.as_view(
        url=static('images/favicon.ico')
    )),
    path('', home.home_view, name='home_view'),
    path('login/', login.login_view, name='login_view'),
    path('auth/', login.do_login, name='do_login'),
    path('duo/', login.do_duo, name='do_duo'),
    path('logout/', login.do_logout, name='do_logout'),
    path('admin/', admin.site.urls, name='django_admin'),
]
