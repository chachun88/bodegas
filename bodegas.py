#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import pymongo
import urllib

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from basehandler import BaseHandler
from globals import port, debugMode, domainName, carpeta_img, userMode, Menu, token, webservice_url

from home_handler import HomeHandler
from login_handler import LoginHandler
from product_add_handler import ProductAddHandler
from product_list_handler import ProductListHandler

from cellar_handler import CellarHandler
from cellar_add_handler import CellarAddHandler

from user_handler import UserHandler, UserRemoveHandler
from user_add_handler import UserAddHandler, UserEditHandler

from report_handler import ReportHandler

#something
define("port", default=port, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):


        settings = dict(
            blog_title=u"Pricecom",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o",
            login_url="/auth/login",
            debug=True,
        )

        handlers = [
            (r"/auth/login", LoginHandler),

            # products
            (r"/", HomeHandler),
            (r"/product/add", ProductAddHandler),
            (r"/product/list", ProductListHandler),

            # cellar
            (r"/cellar", CellarHandler),
            (r"/cellar/add", CellarAddHandler),

            # user
            (r"/user", UserHandler),
            (r"/user/add", UserAddHandler),
            (r"/user/remove", UserRemoveHandler),
            (r"/user/edit", UserEditHandler),

            #report
            (r"/report/cellar", ReportHandler)
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers

        self.side_menu = [
                        {"class":"panel", "name":Menu.PRODUCTOS, "icon":"home", "link":"/", 
                            "sub_menu":[
                                        {"class":"", "name":Menu.PRODUCTOS_CARGA_MASIVA, "link":"/"},
                                        {"class":"", "name":Menu.PRODUCTOS_CARGA, "link":"/product/add"},
                                        {"class":"", "name":Menu.PRODUCTOS_LISTA, "link":"/product/list"}
                                        ]},
                        {"class":"panel", "name":Menu.BODEGAS, "icon":"table", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.BODEGAS_LISTAR, "link":"/cellar"},
                                        {"class":"", "name":Menu.BODEGAS_AGREGAR, "link":"/cellar/add"}
                                        ]},
                        {"class":"panel", "name":Menu.USUARIOS, "icon":"asterisk", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.USUARIOS_LISTAR, "link":"/user"},
                                        {"class":"", "name":Menu.USUARIOS_AGREGAR, "link":"/user/add"}
                                        ]},
                        {"class":"panel", "name":Menu.INFORMES, "icon":"bar-chart-o", "link":"/report",
                            "sub_menu":[
                                        {"class":"", "name":Menu.INFORMES_POR_BODEGA, "link":"/report/cellar"}
                                        ]},
                        {"class":"panel", "name":Menu.SALIR, "icon":"sign-out", "link":"/auth/login"},]


        ## initializing token
        url = webservice_url + "/access_token?appid=100"
        token = urllib.urlopen(url).read()
        print token



def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()