"""
api.py

"""
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.resources import ALL
from tastypie.fields import DictField
from mongoengine.django.auth import User
from tastypie_mongoengine import resources
from bson.objectid import ObjectId

from hopscotch.mongo_tastypie.auth import MongoAuthentication, MongoAuthorization
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
        allowed_methods = ('get', 'post', 'put', 'delete')
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
        allowed_methods = ('get', 'post', 'put', 'delete')
        resource_name = 'checkin'
        authorization = Authorization()
        filtering = {
            'name': ALL,
            'id': ALL,
            'drink_id': ALL,
            'user_id': ALL,
        }

    def dehydrate_drink(self, bundle):
        print bundle.obj.drink_id
        try:
            drink = Drink.objects.get(id=bundle.obj.drink_id)
            dehydrate_dict = drink._data.copy()
            dehydrate_dict.pop(None)
            dehydrate_dict['id'] = drink.id
            return(dehydrate_dict)
        except AttributeError:
            return(None)

# class UserResource(resources.MongoEngineResource):
#   """
#   A user resource

#   """
#   class Meta:
#       queryset = User.objects.all()
#       allowed_methods = ('get', 'post', 'put', 'delete')
#       authorization = Authorization()
