"""
context_processors.py

Custom context processor for managing static files
"""
from django.db import settings
import json

def static(request):
    """
    Static items loaded from config for template
    """     
    with open('%s/hopscotch/dram/%s' % (settings.PROJECT_ROOT, settings.CONFIG_JSON),'rb') as config_file:
        config = json.loads(config_file.read())

    return({
        'js': config['js'],
        'css': config['css'],
        'static_url': config['static_url']
    })
