# Python Standard Library

# Mongo Libs
from mongoalchemy.document import Document
from mongoalchemy import fields

# Local lib


RATING = (
    ('1','1',),
    ('2','2',),
    ('3','3',),
    ('4','4',),
    ('5','5',),
)

class BaseDocument(Document):
    '''
    A base class that all Dram classes will inherit from
    '''
    created = fields.DateTimeField(required=False)
    modified = fields.DateTimeField(required=False)

class Drink(BaseDocument):
    '''
    Represents a single drink.
    '''
    ## Information
    # The canonical name of the drink
    #   Will be shown on the page
    name = fields.StringField()
    maker = fields.StringField(required=False)
    
    # Distillery, brewery, etc
    maker_type = fields.StringField(required=False)
    drink_type = fields.StringField(required=False)
    
    # Actual bottled year, i.e., 1996
    age = fields.IntField(required=False)
    # Exact Date drink released to the public
    release_date = fields.DateTimeField(required=False)
    # Manufacturer's description, often listed on the bottle
    manu_desc = fields.StringField(required=False)
    
    ## Personal/rating information
    # Personal description, from experience
    personal_desc = fields.StringField(required=False)
    rating = fields.IntField(required=False)

    # state of drinking
    enjoying = fields.BoolField(required=False)
    own = fields.BoolField(required=False)
    # Information representing the location queried
    #   against the Foursquare API
    # location = fields.DictField()
