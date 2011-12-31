# Standard Django Libraries
from django import models

# Local Django Libraries
from hopscotch.apps.base import BaseModel
from hopscotch.apps.geo.models import Country, Location

class Distillery(BaseModel):
    
