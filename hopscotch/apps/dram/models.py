# Standard Django Libraries
from django.db import models

# Local Django Libraries
from hopscotch.apps.base import BaseModel

# Location and Meta Information

class PlaceType(BaseModel):
    '''
    Type of place that manufactures drink
        Distillery, Brewery
    '''
    place_type = models.CharField(max_length=255)
    
class Place(BaseModel):
    '''
    Represents a place that makes 
    '''
    place_type = models.ForeignKey(PlaceType)

# Information

RATING = (
    ('1','Don\'t try',),
    ('2','Not bad',),
    ('3','Good',),
    ('4','Delicious',),
    ('5','Must have',),
)
class DrinkType(BaseModel):
    '''
    Type of drink: beer, whiskey
    '''
    drink_type = models.CharField(max_length=255)
    
class Drink(BaseModel):
    '''
    Represents a single drink.
    '''
    ## Information
    # The canonical name of the drink
    #   Will be shown on the page
    full_name = models.CharField(max_length=255)
    place = models.ForeignKey(Place)
    drink_type = models.ForeignKey(DrinkType)
    # Actual bottled year, i.e., 1996
    year = models.IntegerField()
    # Exact Date drin released to the public
    release_date = models.DateField(null=True, default=None)
    # Manufacturer's description, often listed on the bottle
    manu_desc = models.TextField(null=True, blank=True, default='')
    
    ## Personal/rating information
    # Personal description, from experience
    personal_desc = models.TextField(null=True, blank=True, default='')
    
    rating = models.CharField(null=True, blank=True, max_length=1, choices=RATING)
    
    # state of drinking
    #! NOTE: Do we need to set some sort of expiration
    #! ISSUE #1
    enjoying = models.BooleanField()
    own = models.BooleanField()