"""
urls.py

"""

from django.conf.urls import patterns, url, include
from tastypie.api import Api
from hopscotch.dram.api import DrinkResource

v1_api = Api(api_name='v1')
v1_api.register(DrinkResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)