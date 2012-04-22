# Third Party Libraries
from flask import render_template
from flask.views import View
from mongoengine import connect
# Local
from hopscotch.dram.documents import Drink, User

connect('hopscotch')

class BaseView(View):
    methods         = ['GET']

class Home(BaseView):
    def dispatch_request(self, username=None):
        return render_template('home.html')

class Checkin(BaseView):
    def dispatch_request(self, username=None):
        return render_template('checkin.html')

class Cellar(BaseView):
    '''
    Show the drinks in the collection
    '''
    def dispatch_request(self, username=None):
        
        context = {
            'user': [],
            'drinks': []
        }
        
        user = User.objects.get(username=username)
        context['user'] = user
        
        for drink in user.drinks:
            context['drinks'].append(Drink.objects.get(drink_id=drink))
            
            
        return render_template('cellar.html', **context)

class PublicFeed(BaseView):
    """
    Show drinks recently bought or checked-in to.
    """
    def dispatch_request(self):
        pass