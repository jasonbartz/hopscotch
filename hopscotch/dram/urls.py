"""
urls.py

"""

from django.conf.urls import patterns, url, include
from django.shortcuts import render_to_response
from tastypie.api import Api

from hopscotch.dram.api import (DrinkResource,
                                CheckinResource,
                                PublicResource)
from hopscotch.dram.views import (Home,
                                  Public,
                                  Create,
                                  Login,
                                  Logout,
                                  UserHome,
                                  UserPass,
                                  Checkin,
                                  Search,
                                  Enjoying,
                                  Following,
                                  Cellar,
                                  Beta,
                                  Account,
                                  DrinkView)


# API URLs
v1_api = Api(api_name='v1')
v1_api.register(DrinkResource())
v1_api.register(CheckinResource())
v1_api.register(PublicResource())


urlpatterns = patterns('',
    # Public pages
    (r'^$', Home.as_view()),
    (r'^public/$', Public.as_view()),

    # Account pages
    (r'^login/$', Login.as_view()),
    (r'^logout/$', Logout.as_view()),
    (r'^change_password/$', UserPass.as_view()),

    # Creation pages
    (r'^search/$', Search.as_view()),
    (r'^create/$', Create.as_view()),
    (r'^checkin/$', Checkin.as_view()),

    # Drink pages
    (r'^drink/(?P<slug>[\w\d-]+)/(?P<id>[\w\d]+)/$', DrinkView.as_view()),

    # User pages
    (r'^user/(?P<username>\w+)/$', UserHome.as_view()),
    (r'^user/(?P<username>\w+)/enjoyed/$', Enjoying.as_view()),
    (r'^user/(?P<username>\w+)/following/$', Following.as_view()),
    (r'^user/(?P<username>\w+)/cellar/$', Cellar.as_view()),
    (r'^user/(?P<username>\w+)/account/$', Account.as_view()),

    # API
    (r'^api/', include(v1_api.urls)),

    # Beta
    (r'^beta/$', Beta.as_view()),

)