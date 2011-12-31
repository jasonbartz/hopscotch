# Django Standard Libraries
from django.contrib import admin

from hopscotch.apps.dram.models import (Whiskey, 
                                        Distributor, 
                                        Distillery,
                                        WhiskeyType,
                                        Enjoying,)

admin.site.register(Whiskey)
admin.site.register(Distributor)
admin.site.register(Distillery)
admin.site.register(WhiskeyType)
admin.site.register(Enjoying)
