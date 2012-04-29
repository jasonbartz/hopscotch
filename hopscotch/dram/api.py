"""
api.py

"""
from tastypie.authorization import Authorization
from tastypie.resources import ALL
from mongoengine.django.auth import User
from tastypie_mongoengine import resources

from hopscotch.mongo_tastypie.auth import MongoAuthentication, MongoAuthorization
from hopscotch.dram.documents import Drink



# class Public(resources.MongoEngineResource):
# 	"""
# 	A resource for the public feed.
# 	"""

# 	def get_queryset(self):
# 		return Drink.objects.all()

# class MongoResource(resources.MongoEngineResource):


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
		}


# class UserResource(resources.MongoEngineResource):
# 	"""
# 	A user resource

# 	"""
# 	class Meta:
# 		queryset = User.objects.all()
# 		allowed_methods = ('get', 'post', 'put', 'delete')
# 		authorization = Authorization()
