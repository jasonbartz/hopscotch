'''
A generic library that holds base configurations including
    Models and Views

'''

# Standard Django Libraries
from django import models

class BaseModel(models.Model):
    '''
    A base class that most models in the child apps
        will inherit
    '''
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    
    class Meta
        abstract = True