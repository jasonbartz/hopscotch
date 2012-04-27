"""
auth.py

Custom Authentication/Authorization classes for MongoDB

"""
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

class MongoAuthentication(Authentication):
    """
    A login-based authentication route.

    Relevant information is stored in a 
        User collection.
    """
    def is_authenticated(self, request, **kwargs):
        """
        Determines if a user is authenticated.
        """
        return False

    def get_identifier(self, request):
        """
        Identifies the user
        """
        return request.user.username

class MongoAuthorization(Authorization):
    """
    A login-based authorization route.

    Relevant information is stored in a 
        User collection.
    """
    def is_authorized(self, request, object=None):
        """
        Determines if a user is authorized.
        """
        return False

    def apply_limits(self, request, object_list):
        """
        Applies limits to the user
        """
        if request and hasattr(request, 'user'):
            return object_list.filter(author__username=request.user.username)

        return object_list.none()