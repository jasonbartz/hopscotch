# Standard Django Libraries
from django.db import models

# Local Django Libraries
from hopscotch.apps.base import BaseModel

class GeographyBase(BaseModel):
    '''
    A base class for the geograph models
    '''
    # Replace with PostGIS instances
    
    # Currently represents the centroid of a place
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    
    class Meta:
        abstract = True
        
class Country(GeographyBase):
    '''
    A canonical entry that represents a country
    '''
    pass
    
class Area(GeographyBase):
    '''
    A canonical entry that represents a part of a country,
        i.e., a state or province
    '''
    area_type = models.CharField(max_length=255)
    
class Location(GeographyBase):
    '''
    A canonical entry that represents a location, i.e.,
        a city, brewery or distillery
    '''
    area = models.ForeignKey(Area)
    