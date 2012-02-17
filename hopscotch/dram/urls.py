'''
Main URLS file, will direct to proper apps
'''
# Standard Django Libraries
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    # Admin, remove for prod
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    
    # apps
    url(r'^dram/', include('hopscotch.apps.dram.urls')),
)