# Python Standard Library
import datetime
# Mongo Libs
from mongoengine import Document
from mongoengine import fields
from mongoengine.django import auth

RATING = (
    ('1','1',),
    ('2','2',),
    ('3','3',),
    ('4','4',),
    ('5','5',),
)

class Drink(Document):
    '''
    Represents a single drink.
    '''
    created         = fields.DateTimeField(default=datetime.datetime.now())
    modified        = fields.DateTimeField(default=datetime.datetime.now())

    # Meta
    created_by_user = fields.IntField()
    drink_id        = fields.StringField()
    ## Information
    # The canonical name of the drink
    #   Will be shown on the page
    name            = fields.StringField()
    maker           = fields.StringField()
    
    # Distillery, brewery, etc
    maker_type      = fields.StringField()
    drink_type      = fields.StringField()
    
    # Actual bottled year, i.e., 1996
    age             = fields.IntField()
    # Exact Date drink released to the public
    release_date    = fields.DateTimeField(default=datetime.datetime.now())
    # Manufacturer's description, often listed on the bottle
    manu_desc       = fields.StringField()

class UserDrink(Document):
    """
    A drink tied to a user
    """
    drink_id        = fields.StringField()
    user_id         = fields.StringField()

    ## Personal/rating information
    # Personal description, from experience
    personal_desc   = fields.StringField()
    rating          = fields.IntField()

    # state of drinking
    enjoying        = fields.BooleanField(default=False)
    own             = fields.BooleanField(default=False)
    # Information representing the location queried
    #   against the Foursquare API
    # location = fields.DictField()

    def get_recent_checkins(self):

        return('')

class User(auth.User):

    drinks = fields.ListField()
  