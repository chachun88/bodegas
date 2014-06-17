'''
Created on 13/12/2012

@author: ricardo
'''
import tornado.web
from lputils import MoneyFormat
from bson import json_util
#from loadingplay.multilang.lang import lpautoSelectCurrentLang

class BaseHandler(tornado.web.RequestHandler):

    @property
    def referer(self):
        # TODO: deberia guardar el old referer en una variable de session
        self._referer = self.request.headers['Referer']
        self._referer = self._referer.replace("/auth/loadingplay", "/").replace("/registrar/usuario", "/")

        return self._referer

    @property
    def db(self):
        return self.application.db

    @property
    def side_menu(self):
        return self.application.side_menu


    def set_active(self, active_name):
        for x in self.side_menu:
            x["class"] = "panel"
            if x["name"] == active_name:
                x["class"] += " active"

            if "sub_menu" in x:
                for y in x['sub_menu']:
                    y['class'] = ""
                    if y["name"] == active_name:
                        #print "llegaaaa"
                        x["class"] += " active"
                        y["class"] = " active"

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)
        
        # detecto el lenguage del navegador del usuario
        #lpautoSelectCurrentLang(self)
    
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")        
        if not user_json: return None
        return tornado.escape.json_decode(user_json)
    
    def get_usuarios(self):
        return self.db.user.find({"picture":{"$exists":True}}).limit(24)
    
    def get_login_url(self):
        return u"/auth/login"

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

    def get_user_email(self):
        json_data = json_util.loads( self.get_secure_cookie("user") )

        return json_data["email"]

    def render(self, template_name ,**kwargs):

        # global vars
        kwargs["MoneyFormat"] = MoneyFormat
        kwargs["side_menu"] = self.side_menu

        ## overrided method
        tornado.web.RequestHandler.render(self, template_name, **kwargs)

    '''
    def write_error(status_code=500, **kwargs):
        self.write("llega")
    '''

