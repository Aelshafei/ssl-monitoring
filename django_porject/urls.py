"""django_porject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import ssl_monitoring.views

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin' ),
    url(r'^dasboard/', ssl_monitoring.views.index),
    url(r'^services_list/', ssl_monitoring.views.services_list, name='services_list'),
    url(r'^$', ssl_monitoring.views.index, name="index"),
    url(r'^instant_check/(?P<url>.*)$', ssl_monitoring.views.instant_check),
    url(r'^how_to/', ssl_monitoring.views.how_to, name='how_to')
]


admin.site.site_header = 'SSL Review Certificate Review 2.0 Control Panel'
