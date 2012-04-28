"""
api.py 

A lightweight implementation of django-tastypie to GET/POST to MongoDB

UNFINISHED: REPLACED WITH django-tastypie-mongoengine
"""

from tastypie.resources import Resource, DeclarativeMetaclass
from tastypie import fields
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


# class MongoEngineDeclarativeClass(DeclarativeMetaclass):

#     def __new__(cls, name, bases, attr):

#         meta = attrs.get('Meta')


#         if meta and hasattr(meta, 'document'):
#             setattr(cls, 'document', meta.queryset.model)

#         new_class = super(ModelDeclarativeMetaclass, cls).__new__(cls, name, bases, attrs)
#         include_fields = getattr(new_class._meta, 'fields', [])
#         excludes = getattr(new_class._meta, 'excludes', [])
#         field_names = new_class.base_fields.keys()

#         for field_name in field_names:
#             if field_name == 'resource_uri':
#                 continue
#             if field_name in new_class.declared_fields:
#                 continue
#             if len(include_fields) and not field_name in include_fields:
#                 del(new_class.base_fields[field_name])
#             if len(excludes) and field_name in excludes:
#                 del(new_class.base_fields[field_name])

#         # Add in the new fields.
#         new_class.base_fields.update(new_class.get_fields(include_fields, excludes))

#         return new_class

class MongoResource(Resource):
    """
    A class that can be subclassed in order to plug a mongo document
        resource directly into an API
    """

    __metaclass__ = MongoEngineDeclarativeClass

    class Meta:
        database = None
        collection = None

    def _connect(self):
        """
        Connect to a mongo instance.

        Call per method so that it will avoid Mongo reconnect errors.
        """
        connection = MongoConnection(
                    database=self._meta.database,
                    collection=self._meta.collection
                 )
        
        return(connection.connect())

    @classmethod
    def get_mongoenginefields_from_api_fields(self, f, default=fields.CharField):
        pass

    @classmethod
    def get_fields(cls, fields=None, excludes=None):
        pass

    def get_resource_uri(self, bundle_or_obj):
        """
        A method that returns the URI for an indvidual object
    
        Uses the `ObjectID` as the id in the URI
        """
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        kwargs['pk'] = bundle_or_obj.obj.get('_id').__str__()

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

    def full_dehydrate(self, bundle):
        """
        Given a bundle with an object instance, extract the information from it
        to populate the resource.
        """
        self.fields.update(self._meta.document._fields.copy())
        import pdb;pdb.set_trace()
        return(super(MongoResource, self).full_dehydrate(bundle))

    def get_object_list(self, request):
        """
        A method to return a list of objects.
        """
        connection = self._connect()

        mongo_list_cursor = connection.find()

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
        connection = self._connect()

        bundle.obj = connection.save(kwargs)

        bundle = self.full_hydrate(bundle)

        return(bundle)

    def obj_update(self, request=None, **kwargs):
        """
        A method to update an object
        """
        return(self.obj_create(bundle, request, **kwargs))

    def obj_delete(self, request=None, **kwargs):
        """
        A method to delete a single object.
        """
        connection = self._connect()

        failure = connection.remove(**kwargs)

    def obj_delete_list(self, request=None, **kwargs):
        """
        A method to delete an entire list of objects

        UNUSED: Required to override.
        """
        pass

    def rollback(self, bundles):
        """
        A method to rollback failed database transactions.

        UNUSED: Required to override.
        """
        pass