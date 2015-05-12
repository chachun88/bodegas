#!/usr/bin/python
# -*- coding: UTF-8 -*-


import functools
import tornado.web
from bson import json_util

def authenticated(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # objeto = {"cellar_permissions": [1,2,3,4,5,6]}
        # # self.current_user(objeto)
        # self.set_secure_cookie("user_bodega", json_util.dumps(objeto))
        return method(self, *args, **kwargs)
    return wrapper


tornado.web.authenticated = authenticated
