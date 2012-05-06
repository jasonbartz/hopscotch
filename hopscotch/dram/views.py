import json

from django.views.generic import TemplateView
from django.db import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.validators import validate_email, ValidationError
from django.template import RequestContext
from mongoengine import connect

from hopscotch.dram.documents import Drink, User


class BaseView(TemplateView):
    pass

class Home(BaseView):
    template_name = 'home.html'
    
class Public(BaseView):
    template_name = 'public.html'

class Logout(BaseView):
    template_name = 'login.html'
    
    def render_to_response(self, context, **response_kwargs):
        logout(self.request)
        return(super(Logout, self).render_to_response(context, **response_kwargs))

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

class Cellar(BaseView):
    template_name = 'user/cellar.html'

class Enjoying(BaseView):
    template_name = 'user/enjoyed.html'

class Following(BaseView):
    template_name = 'user/following.html'

class UserHome(BaseView):
    template_name = 'user/home.html'

class Beta(BaseView):
    """
    A master view class to handle Beta reponses.

    Currently accepts email addresses and sends them to the administrator.
    """
    template_name = 'beta.html'

    def post(self, request, *args, **kwargs):
        return(self.render_to_response(self.get_context_data(**kwargs), **kwargs))

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """

        if self.request.user.is_authenticated():

            return(redirect(to='/user/%s/' % self.request.user.username))
        
        if self.request.method.upper() in ('POST', 'PUT'):
            try:
                validate_email(self.request.POST['email'])
            except ValidationError, e:
                return render_to_response('home.html',
                                         {'error':'Please enter a valid email address'},
                                         context_instance = RequestContext(self.request))
                
            send_mail('[Beta Sign up]', 
                        'Beta invite request from %s' % self.request.POST['email'],
                        '%s' % self.request.POST['email'],
                        ['accounts@hpsct.ch'], 
                        fail_silently=False)
            return(super(Beta, self).render_to_response(context, **response_kwargs))
        
        else:
            return(redirect(to='/'))
   
