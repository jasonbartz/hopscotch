# Third Party Libraries
from flask import render_template
from flask.views import View

from mongoalchemy.session import Session

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
        
        context = {}
        context['drinks'] = []
        
        query = session.query(User).filter(User.user_id == user_id).limit(10)
        
        for query_obj in query:
            context['drinks'].append(query_obj)
            
        return render_template('cellar.html')

