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
from hopscotch.dram.documents import Drink, UserDrink



# class Public(resources.MongoEngineResource):
#   """
#   A resource for the public feed.
#   """

#   def get_queryset(self):
#       return Drink.objects.all()

# class MongoResource(resources.MongoEngineResource):


# class MongoResource(resources.MongoEngineResource):
#     def put_list(self, request, **kwargs):
        
#         import pdb;pdb.set_trace()
#         deserialized = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT_TYPE', 'application/json'))
#         deserialized = self.alter_deserialized_list_data(request, deserialized)
#         super(MongoResource, self).put_list(request, **kwargs)

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

class UserDrinkResource(resources.MongoEngineResource):
    """
    A resource for drinks.

    """
    drink = DictField()
    class Meta:
        queryset = UserDrink.objects.all()
        allowed_methods = ('get', 'post', 'put', 'delete')
        resource_name = 'userdrink'
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
