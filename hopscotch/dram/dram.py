# Standard Library
import json

# Third Party Libraries
from flask import Flask
from werkzeug.routing import Map, Rule

# Local Libraries
from hopscotch.dram.views import Home, Checkin, Cellar
from hopscotch import exceptions
from hopscotch.settings import PROJECT_ROOT

class Dram(object):
    '''
    A class that holds all of the settings for this app
    '''
    def __init__(self, *args, **kwargs):
        '''
        Initialize the Dram App object
        '''
        self.args = args
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        if not kwargs.get('database'):
            self.database = None
            
        self.run()
    
    def get_urls(self):
        url_mapping = Map([
            Rule('/<string:username>/', endpoint='home_view'),
            Rule('/<string:username>/checkin/', endpoint='checkin_view'),
            Rule('/<string:username>/cellar/', endpoint='cellar_view'),
        ])
        url_functions = {
            'home_view': Home.as_view('home_view'),
            'checkin_view': Checkin.as_view('checkin_view'),
            'cellar_view': Cellar.as_view('cellar_view'),
        }
        
        return url_mapping, url_functions
        
    def _instantiate_app_object(self):
        '''
        Instantiate the Flask object
        '''
        
        self.dram = Flask(__name__)
        
    def _set_environment(self):
        '''
        Configure the environment variables and globals
        '''
        with open('%s/hopscotch/dram/config.json' % PROJECT_ROOT,'rb') as config_file:
            self.config = json.loads(config_file.read())

        self.dram.jinja_env.globals.update({
            'js': self.config['js'],
            'css': self.config['css'],
            'static_url': self.config['static_url']
        })
        self.dram.create_jinja_environment()
        
    def run(self):
        '''
        Run the dram app
        '''
        self._instantiate_app_object()
        self._set_environment()
        
        # URLS
        url_mapping, url_functions = self.get_urls()
        self.dram.url_map = url_mapping
        self.dram.view_functions = url_functions
