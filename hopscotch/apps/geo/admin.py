# Django Standard Libraries
from django.contrib import admin

from hopscotch.apps.geo.models import (Country, 
                                        Area, 
                                        Location,)

admin.site.register(Country)
admin.site.register(Area)
admin.site.register(Location)
