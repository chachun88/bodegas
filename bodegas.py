#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from globals import port, Menu

from home_handler import HomeHandler
from home_handler import ProductRemoveHandler
from home_handler import ProductLoadHandler, ProductOutHandler, ProductMassiveOutputHandler
from login_handler import LoginHandler
from login_handler import LoginPassHandler
from product_add_handler import ProductAddHandler, FastEditHandler, ForSaleHandler, CheckStockHandler
from product_add_handler import ProductEditHandler
from product_list_handler import ProductListHandler
from product_search_handler import ProductSearchHandler

from cellar_handler import CellarHandler, CellarEasyHandler
from cellar_handler import CellarInputHandler
from cellar_handler import CellarOutputHandler
from cellar_handler import CellarDetailHandler, CellarComboboxHandler
from cellar_handler import CellarEasyInputHandler
from cellar_handler import CellarEasyOutputHandler, SelectForSaleHandler, SelectReservationHandler

from order_handler import OrderHandler, AddOrderHandler, OrderActionsHandler

from cellar_add_handler import CellarAddHandler
from cellar_remove_handler import CellarRemoveHandler

from user_handler import UserHandler, UserRemoveHandler
from user_add_handler import UserAddHandler

from report_handler import ReportHandler, ReportUploadHandler

from image_handler import ImageHandler, ImageHandler2, ImageDeleteHandler

from order_detail_handler import AddOrderDetailHandler, ListOrderDetailHandler

from customer_handler import CustomerHandler, CustomerSaveHandler, CustomerActionsHandler, CustomerAddContactHandler, CustomerViewContactHandler, ContactActionsHandler, EditContactHandler

import tag_handler
import shipping_handler

# something
define("port", default=port, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):

        settings = dict(
            blog_title=u"Bodegas",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o",
            login_url="/auth/login",
            debug=True,
        )

        handlers = [
            (r"/auth/login", LoginHandler),
            (r"/auth/recover", LoginPassHandler),

            # products
            # (r"/", HomeHandler),
            (r"/product", HomeHandler),
            (r"/product/out", ProductOutHandler),
            (r"/product/massiveoutput", ProductMassiveOutputHandler),
            (r"/product/load", ProductLoadHandler),
            (r"/product/add", ProductAddHandler),
            (r"/product/list", ProductListHandler),
            (r"/product/edit", ProductEditHandler),
            (r"/product/remove", ProductRemoveHandler),
            (r"/product/search", ProductSearchHandler),
            (r"/product/fastedit", FastEditHandler),
            (r"/product/for_sale", ForSaleHandler),
            (r"/product/checkstock", CheckStockHandler),

            # cellar
            (r"/cellar", CellarHandler),
            (r"/cellar/add", CellarAddHandler),
            (r"/cellar/remove", CellarRemoveHandler),
            (r"/cellar/input", CellarInputHandler),
            (r"/cellar/easyinput", CellarEasyInputHandler),
            (r"/cellar/easyoutput", CellarEasyOutputHandler),
            (r"/cellar/output", CellarOutputHandler),
            (r"/cellar/detail", CellarDetailHandler),
            (r"/cellar/combobox", CellarComboboxHandler),
            (r"/cellar/selectforsale", SelectForSaleHandler),
            (r"/cellar/selectreservation", SelectReservationHandler),
            (r"/cellar/easy", CellarEasyHandler),

            # order
            (r"/order/list", OrderHandler),
            (r"/order/save", AddOrderHandler),
            (r"/orders/actions", OrderActionsHandler),

            # order_detail
            (r"/order-detail/save", AddOrderDetailHandler),
            (r"/order-detail/list", ListOrderDetailHandler),

            # user
            (r"/user", UserHandler),
            (r"/user/add", UserAddHandler),
            (r"/user/remove", UserRemoveHandler),
            (r"/user/edit", UserAddHandler),

            # report
            (r"/", ReportHandler),
            (r"/report/upload", ReportUploadHandler),
            (r"/report/download/([^/]+)", tornado.web.StaticFileHandler, {'path': 'uploads/'}),

            # images
            (r"/image/([^/]+)", ImageHandler),
            (r"/image", ImageHandler2),
            (r"/image/", ImageHandler2),
            (r"/imageremove", ImageDeleteHandler),

            # customer
            (r"/customer", CustomerHandler),
            (r"/customer/save", CustomerSaveHandler),
            (r"/customer/actions", CustomerActionsHandler),
            (r"/customer/add_contact", CustomerAddContactHandler),
            (r"/customer/view_contact", CustomerViewContactHandler),

            (r"/contact/actions", ContactActionsHandler),
            (r"/customer/edit_contact", EditContactHandler),

            (r"/tag/list",              tag_handler.TagHandler),
            (r"/tag/remove",            tag_handler.RemoveHandler),
            (r"/tag/edit",              tag_handler.EditHandler),
            (r"/tag/hideshow",          tag_handler.HideShowHandler),
            (r"/tag/add",               tag_handler.AddHandler),

            (r"/shipping/list",         shipping_handler.ListHandler),
            (r"/shipping/save",         shipping_handler.SaveHandler),
            (r"/shipping/savecity",     shipping_handler.AddCityHandler),
            (r"/shipping/action",       shipping_handler.ActionHandler),
            (r"/shipping/remove",       shipping_handler.RemoveHandler),
            (r"/shipping/save_tracking",       shipping_handler.SaveTrackingCodeHandler)
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers

        self.side_menu = [
                        {"class":"panel", "name":Menu.INFORMES, "icon":"bar-chart-o", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.INFORMES_POR_BODEGA, "link":"/"}
                                        ]},
                        {"class":"panel", "name":Menu.PRODUCTOS, "icon":"home", "link":"/product", 
                            "sub_menu":[
                                        {"class":"", "name":Menu.PRODUCTOS_LISTA, "link":"/product/list"},
                                        {"class":"", "name":Menu.PRODUCTOS_CARGA, "link":"/product/add"},
                                        {"class":"", "name":Menu.PRODUCTOS_CARGA_MASIVA, "link":"/product/out"}
                                        ]},
                        {"class":"panel", "name":Menu.CLIENTES, "icon":"users", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.CLIENTES_LISTAR, "link":"/customer"}
                                        ]},
                        {"class":"panel", "name":Menu.PEDIDOS, "icon":"truck", "link":"/order", 
                            "sub_menu":[
                                        {"class":"", "name":Menu.PEDIDOS_LISTA, "link":"/order/list"}
                                        ]},
                        {"class":"panel", "name":Menu.BODEGAS, "icon":"table", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.BODEGAS_LISTAR, "link":"/cellar"},
                                        {"class":"", "name":Menu.BODEGAS_AGREGAR, "link":"/cellar/add"},
                                        {"class":"", "name":Menu.PRODUCTOS_CARGA_STOCK, "link":"/product"},
                                        {"class":"", "name":Menu.BODEGAS_FACIL, "link": "/cellar/easy"}
                                        ]},
                        {"class":"panel", "name":Menu.CONFIGURACION, "icon":"cog", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.BODEGAS_FORSALE, "link":"/cellar/selectforsale"},
                                        {"class":"", "name":Menu.BODEGAS_RESERVATION, "link":"/cellar/selectreservation"}
                                        ]},
                        {"class":"panel", "name":Menu.USUARIOS, "icon":"asterisk", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.USUARIOS_LISTAR, "link":"/user"},
                                        {"class":"", "name":Menu.USUARIOS_AGREGAR, "link":"/user/add"}
                                        ]},
                        {"class":"panel", "name":Menu.TAGS, "icon":"tags", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.TAGS_LISTAR, "link":"/tag/list"},
                                        {"class":"", "name":Menu.TAGS_ADD, "link":"/tag/add"}
                                        ]},
                        {"class":"panel", "name":Menu.SHIPPING, "icon":"plane", "link":"/",
                            "sub_menu":[
                                        {"class":"", "name":Menu.SHIPPING_LIST, "link":"/shipping/list"},
                                        {"class":"", "name":Menu.SHIPPING_SAVE, "link":"/shipping/save"}
                                        ]},
                        {"class":"panel", "name":Menu.SALIR, "icon":"sign-out", "link":"/auth/login"},]


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()