"""
urls.py

"""

from django.conf.urls import patterns, url, include
from django.shortcuts import render_to_response
from tastypie.api import Api

from hopscotch.dram.api import DrinkResource
from hopscotch.dram.views import Public


# API URLs
v1_api = Api(api_name='v1')
v1_api.register(DrinkResource())


urlpatterns = patterns('',
    (r'^$', Public.as_view()),
    (r'^api/', include(v1_api.urls)),
)