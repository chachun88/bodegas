'''
Created on 13/12/2012

@author: ricardo
'''
import tornado

from bson.objectid import ObjectId
from model10.basemodel import BaseModel

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db
    
    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)

    # validate access token, before send data
    # @return   true if the token is valid
    #           false if the token is invalid
    def ValidateToken(self):

        token = self.get_argument("token","")
        bm = BaseModel()
        response_obj = bm.ValidateToken(token)

        if "success" in response_obj:
            return True
        else:
            # print response_obj["error"]
            return False

    def RemoveItem(self, model, collection):

        # validate access token
        if not self.ValidateToken():
            return ""

        model.RemoveById(self.get_argument("id", ""), collection)

    def GetItem(self, model, collection):
        # validate access token
        if not self.ValidateToken():
            return ""

        return model.FindById(self.get_argument("id", ""), collection)
