"""
api.py 

A lightweight implementation of django-tastypie to GET/POST to MongoDB

"""

from tastypie import Resource
from pymongo import Connection

class MongoConnection(object):
	"""
	A helper class to connect to a database and maintain that connection.
	
	Usage:

	>>> mongo_instance = MongoConnection(database='my_database', collection='my_collection')
	>>> mongo_connection = mongo_instance.connect()
	"""

	def __init__(self, *args, **kwargs):
		"""
		Set defaults and add kwargs
		"""
		self.args = args

		defaults = {
			'host': 'localhost',
			'port': 27017,
			'database': 'test',
			'collection': 'test',
		}
		defaults.update(kwargs)
		
		for key, value in defaults.items():
			setattr(self, key, value)

	def _connect_to_db(self):
		"""
		Connect to host, port, database
		"""
		connection = Connection(self.host, self.port)

		return(connection[self.database])

	def connect(self):
		"""
		Connect to collection
		"""
		database = self._connect_to_db()

		return(database[self.collection]) 

class MongoResource(Resource):
	"""
	A class that can be subclassed in order to plug a mongo document
		resource directly into an API
	"""
	database = None
	collection = None

	def _connect(self):
		return(MongoConnection(
					database=self.database,
					collection=self.collection
				 )
		)

	def get_resource_uri(self, bundle_or_obj):
		"""
		A method that returns the URI for an indvidual object
	
		Uses the `ObjectID` as the id in the URI
		"""
		kwargs = {
            'resource_name': self._meta.resource_name,
        }

        kwargs['pk'] = bundle_or_obj.id

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

	def get_object_list(self, request):
		"""
		A method to return a list of objects.
		"""
		connection = self._connect()

		mongo_list_cursor = connection.find():

		results = []

		for mongo_obj in mongo_list_cursor:
			results.append(mongo_obj)

		return(results)

	def obj_get_list(self, request=None, **kwargs):
		"""
		A method to to enable filtering on a list
		"""
		return(self.get_object_list(request))

	def obj_get(self, request=None, **kwargs):
		"""
		A method required to get a single object
		"""
		connection = self._connect()

		return(connection.find_one(kwargs['pk']))
		
	def obj_create(self, request=None, **kwargs):
		"""
		A method to create an object
		"""
		pass

	def obj_update(self, request=None, **kwargs):
		"""
		A method to update an object
		"""
		pass

	def obj_delete_list(self, request=None, **kwargs):
		"""
		A method to delete an entire list of objects
		"""
		pass

	def obj_delete(self, request=None, **kwargs):
		"""
		A method to delete a single object.
		"""
		pass

	def rollback(self, bundles):
		"""
		A method to rollback failed database transactions.
		"""
		pass