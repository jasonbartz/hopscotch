import datetime

from django.template.defaultfilters import slugify
from mongoengine import Document
from mongoengine import fields
from mongoengine.django import auth

RATING = (
    ('1', '1',),
    ('2', '2',),
    ('3', '3',),
    ('4', '4',),
    ('5', '5',),
)


class Drink(Document):
    '''
    Represents a single drink.
    '''
    modified = fields.DateTimeField(default=datetime.datetime.now())

    # Meta
    created_by_user = fields.IntField()
    drink_id = fields.StringField()

    ## Information
    # The canonical name of the drink
    #   Will be shown on the page
    name = fields.StringField(required=True)
    slug = fields.StringField(required=True)
    maker = fields.StringField()

    # Distillery, brewery, etc
    maker_type = fields.StringField()
    drink_type = fields.StringField()

    # Actual bottled year, i.e., 1996
    age = fields.IntField()
    # Exact Date drink released to the public
    release_date = fields.DateTimeField(default=datetime.datetime.now())
    # Manufacturer's description, often listed on the bottle
    manu_desc = fields.StringField()

    def save(self, safe=True, force_insert=False, validate=True,
             write_options=None,  cascade=None, cascade_kwargs=None,
             _refs=None):
        self.slug = slugify(self.name)
        return(super(Drink, self).save(safe=True, force_insert=False, validate=True,
             write_options=None,  cascade=None, cascade_kwargs=None,
             _refs=None))


class Checkin(Document):
    """
    A drink tied to a user
    """
    created = fields.DateTimeField(default=datetime.datetime.now())

    drink_id = fields.StringField(required=True)
    user_id = fields.StringField(required=True)

    ## Personal/rating information
    # Personal description, from experience
    personal_desc = fields.StringField()
    rating = fields.IntField()

    # state of drinking
    enjoying = fields.BooleanField(default=False)
    own = fields.BooleanField(default=False)
    # Information representing the location queried
    #   against the Foursquare API
    # location = fields.DictField()

    class Meta:
        ordering = ("-created",)

    def __unicode__(self):

        return('%s @ %s' % (self.drink_id, self.user_id))


class User(auth.User):

    drinks = fields.ListField()
