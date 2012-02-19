# Standard Library
import os
import json

# Third Party Libraries
from flask import Flask
from mongoalchemy.session import Session

# Local Libraries
from hopscotch.dram.views import Home, Checkin, Cellar
from hopscotch.dram.api import DocumentResource
from hopscotch.dram.documents import Drink
from hopscotch import exceptions
from hopscotch.settings import PROJECT_ROOT

class Dram(object):

    def __init__(self, *args, **kwargs):
        
        self.args = args
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        if not kwargs.get('database'):
            self.database = None
            
        self.run()
        
    def _open_mongo_session(self):
        if self.database:
            self.session = Session.connect(self.database)
        else:
            raise exceptions.ConfigurationError('Please pass a `database` kwargs')
    
    def _instantiate_app_object(self):
        
        self.dram = Flask(__name__)
        
    def _get_config(self):
        with open('%s/hopscotch/dram/config.json' % PROJECT_ROOT,'rb') as config_file:
            self.config = json.loads(config_file.read())

        self.dram.jinja_env.globals.update({
            'js': self.config['js'],
            'css': self.config['css'],
            'static_url': self.config['static_url']
        })
    def run(self):
        self._open_mongo_session()
        self._instantiate_app_object()
        self._get_config()
        self.dram.create_jinja_environment()

        # URLS
        self.dram.add_url_rule('/', view_func=Home.as_view('home_view'))
        self.dram.add_url_rule('/checkin/', view_func=Checkin.as_view('checkin_view'))
        self.dram.add_url_rule('/cellar/', view_func=Cellar.as_view('cellar_view'))
        
        # SUPER HACKY, need to change
        class DrinkResource(DocumentResource):
            document = Drink
            session = self.session
            app = self.dram
        
        api = DrinkResource()
                
        api.urls('v1')

dram = Dram(database = 'dram')



if __name__ == '__main__':

    dram.dram.run(debug=True)