"""
api.py

"""
from hopscotch.mongo_tastypie.api import MongoResource
from hopscotch.mongo_tastypie.auth import MongoAuthentication, MongoAuthorization

class DrinkResource(MongoResource):
	"""
	A resource for an individual drink.

	"""

	class Meta:
		database = 'hopscotch'
		collection = 'Drink'


class UserResource(MongoResource):
	"""
	A user resource

	"""
	
	class Meta:
		database = 'hopscotch'
		collection = 'User'