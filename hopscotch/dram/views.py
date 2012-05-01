import json

from django.views.generic import TemplateView
from django.db import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from mongoengine import connect

from hopscotch.dram.documents import Drink, User


class BaseView(TemplateView):

    def _get_config(self):
        """
        Get the config json, currently located in hopscotch.dram
        """
        with open('%s/hopscotch/dram/config.json.local' % settings.PROJECT_ROOT,'rb') as config_file:
            self.config = json.loads(config_file.read())
    
    def get_context_data(self, **kwargs):
        
        self._get_config()

        return({
            'js': self.config['js'],
            'css': self.config['css'],
            'static_url': self.config['static_url']
        })


class Home(BaseView):
    template_name = 'home.html'
    
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
        if self.request.user.is_authenticated():

            return(redirect(to='/user/%s/' % self.request.user.username))
        
        if self.request.method in ('POST', 'PUT'):
            
            request_dict = self.request.POST.copy()
            username = request_dict.get('username')
            password =  request_dict.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    self.request.session.set_test_cookie()
                    return(redirect(to='/user/%s/' % username))

                else:
                    pass# Return a 'disabled account' error message
            else:
                pass# Return an 'invalid login' error message.

        
        return(super(Login, self).render_to_response(context, **response_kwargs))

class Create(BaseView):
    template_name = 'create.html'

class Checkin(BaseView):
    template_name = 'user/checkin.html'    

class UserHome(BaseView):
    template_name = 'user/home.html'
