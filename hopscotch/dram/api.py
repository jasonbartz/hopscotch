"""
api.py

"""
import datetime
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ALL
from tastypie.fields import DictField
from tastypie.bundle import Bundle
from tastypie.http import HttpBadRequest
from tastypie.exceptions import ImmediateHttpResponse
from mongoengine.django.auth import User
from tastypie_mongoengine import resources
from bson.objectid import ObjectId
from django.http import HttpResponse, HttpResponseNotFound, Http404

from hopscotch.dram.documents import Drink, Checkin


class PublicResource(resources.MongoEngineResource):
    """
    A resource for the public feed.
    """
    class Meta:
        queryset = Checkin.objects.all()
        allowed_methods = ('get',)


class DrinkResource(resources.MongoEngineResource):
    """
    A resource for drinks.

    """
    class Meta:
        queryset = Drink.objects.all()
        always_return_data = True
        allowed_methods = ('get', 'post', 'put', 'patch')
        authorization = Authorization()
        filtering = {
            'name': ALL,
            'id': ALL,
        }


class CheckinResource(resources.MongoEngineResource):
    """
    A resource for drinks.

    """
    drink = DictField()

    class Meta:
        queryset = Checkin.objects.all()
        always_return_data = True
        allowed_methods = ('get', 'post', 'put', 'delete', 'patch')
        resource_name = 'checkin'
        authorization = Authorization()
        filtering = {
            'name': ALL,
            'id': ALL,
            'drink_id': ALL,
            'user_id': ALL,
            'enjoying': ALL,
            'own': ALL,
        }

    def obj_create(self, bundle, request=None, **kwargs):
        """
        Override the create method to see if a drink was created recently, if so, it returns an error.
        """
        latest_from_user = Checkin.objects.filter(user_id=bundle.data['user_id']).order_by('-created')[0]
        if latest_from_user.created > (datetime.datetime.now() - datetime.timedelta(seconds=30)):
            raise ImmediateHttpResponse(HttpBadRequest("Max checkins in time period reached."))

        return(super(CheckinResource, self).obj_create(bundle, request, **kwargs))

    def dehydrate_drink(self, bundle):
        try:
            drink = Drink.objects.get(id=bundle.obj.drink_id)
            dehydrate_dict = drink._data.copy()
            dehydrate_dict.pop(None)
            dehydrate_dict['id'] = drink.id
            return(dehydrate_dict)

        except AttributeError:
            return(None)


class BackboneCheckin(resources.MongoEngineResource):
    class Meta:
        queryset = Checkin.objects.all()
        always_return_data = True
        allowed_methods = ('get', 'post', 'put', 'delete', 'patch')
        resource_name = 'b_checkin'
        authorization = Authorization()
        filtering = {
            'name': ALL,
            'id': ALL,
            'drink_id': ALL,
            'user_id': ALL,
            'enjoying': ALL,
            'own': ALL,
        }

    def alter_list_data_to_serialize(self, request, data):
        return data["objects"]
