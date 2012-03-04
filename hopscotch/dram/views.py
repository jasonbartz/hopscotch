# Third Party Libraries
from flask import render_template
from flask.views import View
from mongoalchemy.session import Session

# Local
from hopscotch.dram.documents import Drink, User

session = Session.connect('dram')


class BaseView(View):
    methods         = ['GET']

class Home(BaseView):
    def dispatch_request(self):
        return render_template('home.html')

class Checkin(BaseView):
    def dispatch_request(self):
        return render_template('checkin.html')

class Cellar(BaseView):
    '''
    Show the drinks in the collection
    '''
    def dispatch_request(self, user_id=None):
        
        context = {
            'user': [],
            'drinks': []
        }
        
        user = session.query(User).filter(User.user_id == user_id).one()
        context['user'] = user
        
        for drink in user.drinks:
            context['drinks'].append(session.query(Drink).filter(Drink.drink_id == drink).one())
        
            
        return render_template('cellar.html', **context)

