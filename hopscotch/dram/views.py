import json

from django.views.generic import TemplateView
from django.db import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, redirect
from mongoengine import connect
from mongoengine.django.auth import User

from hopscotch.dram.documents import Drink


class BaseView(TemplateView):

    def _get_config(self):
        """
        Get the config json, currently located in hopscotch.dram
        """
        with open('%s/hopscotch/dram/config.json.old' % settings.PROJECT_ROOT,'rb') as config_file:
            self.config = json.loads(config_file.read())
    
    def get_context_data(self, **kwargs):
        
        self._get_config()

        return({
            'js': self.config['js'],
            'css': self.config['css'],
            'static_url': self.config['static_url']
        })


class Public(BaseView):
    template_name = 'public.html'

class Login(BaseView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        return(self.render_to_response({}, **kwargs))
        
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        if self.request.method in ('POST', 'PUT'):
            
            request_dict = self.request.POST.copy()
            username = request_dict.get('username')
            password =  request_dict.get('password')
            print username
            user = User.objects.get(username=username)

            user.check_password(password)
            user.is_authenticated

            return(redirect(to='/user/%s/' % username))
        
        return(super(Login, self).render_to_response(context, **response_kwargs))


class Create(BaseView):
    template_name = 'create.html'

class UserHome(BaseView):
    template_name = 'user/home.html'

class UserCellar(BaseView):
    template_name = 'user/cellar.html'
