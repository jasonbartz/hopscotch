"""
api.py

"""
# from hopscotch.mongo_tastypie.api import MongoResource
from tastypie_mongoengine import resources

from hopscotch.mongo_tastypie.auth import MongoAuthentication, MongoAuthorization
from hopscotch.dram.documents import Drink



class DrinkResource(resources.MongoEngineResource):
	"""
	A resource for an individual drink.

	"""

	class Meta:
		queryset = Drink.objects.all()
		allowed_methods = ('get', 'post', 'put', 'delete')
		# authorization = authorization.Authorization()


# class UserResource(MongoResource):
# 	"""
# 	A user resource

# 	"""
	
# 	class Meta:
# 		database = 'hopscotch'
# 		collection = 'user'