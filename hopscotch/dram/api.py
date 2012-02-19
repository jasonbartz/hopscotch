# Standard Library
import json
import datetime

# Third Party Libraries
from bson.objectid import ObjectId
from bson import json_util
from mongoalchemy.session import Session
from flask.views import View
from flask import jsonify, Response


class InvalidSetup(Exception):
    '''
    Set up incorrectly
    '''
class DocumentBase(object):
    pass
    
class DocumentResource(DocumentBase, View):

    document = None
    session = None
    app = None

    def __init__(self, *args, **kwargs):
        
        self.args = args
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        # self.urls()
    
    def dispatch_request(self, object_id, response=None):
        return(Response(response=self.get_detail(object_id), mimetype='application/json'))
        
    
    def wrap_json(self, api_dict):
        return(json.dumps(api_dict, default=json_util.default))
    
    def detail_view(self, object_id):
        #api_json = self.get_detail(object_id)    
        # response=self.resource.detail_view(object_id)
        # return api_json
        pass
        
    def get_detail(self, object_id):
        
        if not self.document:
            raise InvalidSetup('need document')
        
        if not self.session:
            raise InvalidSetup('need session')
        
        if not self.app:
            raise InvalidSetup('need app')
            
        detail_query = self.session.query(self.document).filter(self.document.mongo_id == ObjectId(object_id)).one()

        document_fields = self.document.get_fields()
        
        api_dict = {}
        
        for field_name in document_fields:
            api_dict[field_name] = getattr(detail_query, field_name)
            
            if isinstance(getattr(detail_query, field_name), datetime.datetime):
                api_dict[field_name] = datetime.datetime.strftime(getattr(detail_query, field_name),'%Y-%m-%d T%H:%M:%S')
        
        return(self.wrap_json(api_dict))
    
    def urls(self, api_name):

        self.app.add_url_rule('/api/%s/detail/<string:object_id>/' % api_name, view_func=self.as_view('detail_view'))
        
