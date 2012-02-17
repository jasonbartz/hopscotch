# Mongo Libs

RATING = (
    ('1','1',),
    ('2','2',),
    ('3','3',),
    ('4','4',),
    ('5','5',),
)
class BaseDocument(object):
    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    
    
class Drink(BaseDocument):
    '''
    Represents a single drink.
    '''
    ## Information
    # The canonical name of the drink
    #   Will be shown on the page
    full_name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    place_type = models.CharField(max_length=255)
    drink_type = models.CharField(max_length=255)
    
    # Actual bottled year, i.e., 1996
    age = models.IntegerField(null=True, default=None)
    # Exact Date drink released to the public
    release_date = models.DateField(null=True, default=None)
    # Manufacturer's description, often listed on the bottle
    manu_desc = models.TextField(null=True, blank=True, default='')
    
    ## Personal/rating information
    # Personal description, from experience
    personal_desc = models.TextField(null=True, blank=True, default='')
    
    rating = models.CharField(null=True, blank=True, max_length=1, choices=RATING)
    
    # state of drinking
    enjoying = models.BooleanField()
    own = models.BooleanField()