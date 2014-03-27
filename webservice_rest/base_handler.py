'''
Created on 13/12/2012

@author: ricardo
'''
import tornado

from bson.objectid import ObjectId
from model.basemodel import BaseModel

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

        access_token = ""
        tokens_dict = dict()
        c = 0

        # validate access token
        try:
            access_token = self.get_argument("token")
            tokens_dict = self.db.access_token.find({"_id": ObjectId(access_token)})

            if tokens_dict.count() > 1:
                raise Exception("token error")

            for token in tokens_dict:
                # TODO: validate token and permissions
                pass

        except Exception, e:
            # self.write(str(e))
            self.write('{"error":"access token not found"}')
            return False

        return True

    def TryGetParam(self, arg_name, default_value):
        try:
            return self.get_argument(arg_name)
        except Exception, e:
            return default_value

    def RemoveItem(self, model, collection):

        # validate access token
        if not self.ValidateToken():
            return ""

        model.RemoveById(self.TryGetParam("id", ""), collection)

    def GetItem(self, model, collection):
        # validate access token
        if not self.ValidateToken():
            return ""

        return model.FindById(self.TryGetParam("id", ""), collection)
