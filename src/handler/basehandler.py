'''
Created on 13/12/2012

@author: ricardo
'''
import tornado.web
from lputils import MoneyFormat
from bson import json_util
from ..model10.user import User
import locale
import os
# from loadingplay.multilang.lang import lpautoSelectCurrentLang


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
                        # print "llegaaaa"
                        x["class"] += " active"
                        y["class"] = " active"

    def __init__(self, application, request, **kwargs):
        tornado.web.RequestHandler.__init__(self, application, request, **kwargs)

        # detecto el lenguage del navegador del usuario
        # lpautoSelectCurrentLang(self)

    ''' @return current user email '''
    def get_current_user(self):
        user_json = self.get_secure_cookie("user_bodega")        
        if user_json: 
            return tornado.escape.json_decode(user_json)
        else:
            return None

    def get_usuarios(self):
        return self.db.user.find({"picture":{"$exists":True}}).limit(24)

    def get_login_url(self):
        return u"/auth/login"

    # def set_current_user(self, user):
    #     if user:
    #         self.set_secure_cookie("user_bodega", tornado.escape.json_encode(user))
    #     else:
    #         self.clear_cookie("user_bodega")

    def get_user_email(self):
        try:
            json_data = json_util.loads( self.get_secure_cookie("user_bodega") )

            return json_data["email"]
        except:
            pass
        return self.get_secure_cookie("user_bodega")

    def CustomDateFormat(self,date):

        return date.strftime('%d/%m/%Y %H:%M')

    @staticmethod
    def money_format(value):

        if os.name != "nt":
            locale.setlocale( locale.LC_NUMERIC, 'es_ES.UTF-8' )
        else:
            locale.setlocale( locale.LC_NUMERIC, 'Spanish_Spain.1252' )
        return "${}".format(locale.format('%d', value, True))

    def render(self, template_name ,**kwargs):

        # loading current_user
        user = User()
        try:
            user.InitWithEmail( self.get_current_user() )
        except:
            pass

        # global vars
        kwargs["MoneyFormat"] = MoneyFormat
        kwargs["side_menu"] = self.side_menu
        kwargs["CustomDateFormat"] = self.CustomDateFormat
        kwargs["money_format"] = self.money_format

        # overrided method
        tornado.web.RequestHandler.render(self, template_name, **kwargs)

    '''
    def write_error(status_code=500, **kwargs):
        self.write("llega")
    '''

    def showError(self, error_text):
        return {'error': error_text}

    def showSuccessMessage(self, message):
        return {'success': message}
