# Python Standard Library

# Mongo Libs
from mongoalchemy.document import Document
from mongoalchemy import fields

# Local lib
from hopscotch.dram.db import Connect

connection = Connect()


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
    created = fields.DateTimeField()
    modified = fields.DateTimeField()

class Drink(BaseDocument):
    '''
    Represents a single drink.
    '''
    ## Information
    # The canonical name of the drink
    #   Will be shown on the page
    name = fields.StringField()
    maker = fields.StringField()
    
    # Distillery, brewery, etc
    maker_type = fields.StringField()
    drink_type = fields.StringField()
    
    # Actual bottled year, i.e., 1996
    age = fields.IntField()
    # Exact Date drink released to the public
    release_date: datetime.datetime,
    # Manufacturer's description, often listed on the bottle
    manu_desc = fields.StringField()
    
    ## Personal/rating information
    # Personal description, from experience
    personal_desc = fields.StringField()
    rating = fields.IntField()

    # state of drinking
    enjoying = fields.BoolField()
    own = fields.BoolField()
    # Information representing the location queried
    #   against the Foursquare API
    location = fields.DictField(),
