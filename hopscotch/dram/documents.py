# Python Standard Library

# Mongo Libs
from mongokit import Document

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
@connection.register
class Drink(Document):
    '''
    Represents a single drink.
    '''
    __collection__ = 'drink'
    __database__ = 'hopscotch'
    structure = {
        created: datetime.datetime,
        modified: datetime.datetime,
        ## Information
        # The canonical name of the drink
        #   Will be shown on the page
        name: unicode,
        maker: unicode,
        # Distillery, brewery, etc
        maker_type: unicode,
        drink_type: unicode
        # Actual bottled year, i.e., 1996
        age: int,
        # Exact Date drink released to the public
        release_date: datetime.datetime,
        # Manufacturer's description, often listed on the bottle
        manu_desc: unicode,
        ## Personal/rating information
        # Personal description, from experience
        personal_desc: unicode,
        rating: int,

        # state of drinking
        enjoying: bool,
        own: bool,
        # Information representing the location queried
        #   against the Foursquare API
        location: dict,
    }