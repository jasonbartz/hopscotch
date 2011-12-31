# Django Standard Libraries
from django.contrib import admin

from hopscotch.apps.dram.models import (PlaceType, 
                                        Place, 
                                        DrinkType,
                                        Drink,)

admin.site.register(PlaceType)
admin.site.register(Place)
admin.site.register(DrinkType)
admin.site.register(Drink)