# Standard Django Libraries
from django import models

# Local Django Libraries
from hopscotch.apps.base import BaseModel
from hopscotch.apps.geo.models import Location

# Location and Meta Information
class Distillery(BaseModel):
    '''
    Represents a place where whiskey is distilled
        Keep in mind, this may not be the same as the distributor
    '''
    
    location = models.ForeignKey(location)
    
class Distributor(BaseModel):
    '''
    Represents the whiskey distributor
    '''
    
    location = models.ForeignKey(location)

# Whiskey information


RATING = (
    ('1','Don\'t try',),
    ('2','Not bad',),
    ('3','Good',),
    ('4','Delicious',),
    ('5','Must have',),
)

class Whiskey(BaseModel)
    '''
    Represents a single whiskey.
    '''
    ## Whiskey Information
    # The canonical name of the whiskey
    #   Will be shown on the page
    full_name = models.CharField(max_length=255)
    
    # Actual bottled year, i.e., 1996
    year = models.IntegerField()
    
    # Exact Date whiskey released to the public
    release_date = models.DateField(null=True, default=None)

    # Manufacturer's description, often listed on the bottle
    manu_desc = models.Textfield(null=True, blank=True, default='')
    
    ## Personal/rating information
    # Personal description, from experience
    personal_desc = models.Textfield(null=True, blank=True, default='')
    
    rating = models.CharField(null=True, blank=True, choices=RATING)
    
    # state of drinking
    #! NOTE: Do we need to set some sort of expiration
    #! ISSUE #1
    enjoying = models.BooleanField(null=True)
    own = models.BooleanField(null=True)