import json

from django.views.generic import TemplateView
from django.db import settings
from mongoengine import connect

from hopscotch.dram.documents import Drink, User


class BaseView(TemplateView):

    def _get_config(self):
        """
        Get the config json, currently located in hopscotch.dram
        """
        with open('%s/hopscotch/dram/config.json' % settings.PROJECT_ROOT,'rb') as config_file:
            self.config = json.loads(config_file.read())
    
    def get_context_data(self, **kwargs):
        
        self._get_config()

        return({
            'js': self.config['js'],
            # 'css': self.config['css'],
            'static_url': self.config['static_url']
        })


class Public(BaseView):
    template_name = 'public.html'

class UserHome(BaseView):
    template_name = 'user/home.html'

class UserCellar(BaseView):
    template_name = 'user/cellar.html'
