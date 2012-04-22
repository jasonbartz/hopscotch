'''
A class for import json fixtures
'''
import json

from mongoengine import register_connection, connect
from hopscotch.settings import PROJECT_ROOT
from hopscotch.dram import documents
from hopscotch.dram.utils.decode import _decode_dict, _decode_list

connect('hopscotch')

class Fixture(object):
    
    def __init__(self, *args, **kwargs):
        
        self.args = args
        
        if not kwargs.get('fixtures'):
            self.fixtures = '%s/hopscotch/dram/fixtures/hopscotch.json' % PROJECT_ROOT
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
        self._load_fixtures()
        
    def _load_fixtures(self):
        
        with open(self.fixtures, 'rb') as open_fixtures:
            self.fixture = json.load(open_fixtures, object_hook=_decode_dict)
    
    def run(self):
        for key, document in self.fixture.items():
            query_document = getattr(documents, key)

            for single_document in document:
                
                query_obj = query_document(**single_document)
                query_obj.save()