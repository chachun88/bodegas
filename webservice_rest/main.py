 #!/usr/bin/env python


from datetime import date
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import pymongo

import access_token
import product_handler
import seller_handler
import brand_handler
import order_handler
import order_detail_handler

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",                      access_token.AccessTokenHandler),
            (r"/access_token",          access_token.AccessTokenHandler),

            (r"/product/add",           product_handler.AddProductHandler),
            (r"/product/edit",          product_handler.AddProductHandler),
            (r"/product/delete",        product_handler.RemoveProductHandler),
            (r"/product/find",          product_handler.GetProductHandler),
            (r"/product/list",          product_handler.ListProductsHandler),

            (r"/salesman/add",          seller_handler.AddSellerHandler),
            (r"/salesman/edit",         seller_handler.AddSellerHandler),
            (r"/salesman/delete",       seller_handler.RemoveSellerHandler),
            (r"/salesman/find",         seller_handler.GetSalesmanHandler),
            (r"/salesman/list",         seller_handler.ListSalesmanHandler),

            (r"/brand/add",             brand_handler.AddBrandHandler),
            (r"/brand/edit",            brand_handler.AddBrandHandler),
            (r"/brand/delete",          brand_handler.RemoveBrandHandler),
            (r"/brand/find",            brand_handler.GetBrandHandler),
            (r"/brand/list",            brand_handler.LisBrandHandler),

            (r"/order/add",             order_handler.AddOrderHandler),
            (r"/order/edit",            order_handler.EditOrderHandler),
            (r"/order/delete",          order_handler.RemoveOrderHandler),
            (r"/order/find",            order_handler.GetOrderHandler),
            (r"/order/list",            order_handler.ListOrderHandler),

            (r"/order-detail/add",      order_detail_handler.OrderDetailHandler),
            (r"/order-detail/edit",     order_detail_handler.OrderDetailHandler),
            (r"/order-detail/delete",   order_detail_handler.RemoveOrderDetailHandler),
            (r"/order-detail/find",     order_detail_handler.GetOrderDetailHandler),
            (r"/order-detail/list",     order_detail_handler.ListOrderDetailHandler),

            (r"/product/file-upload-sample",    product_handler.UploadPictureSampleHandler),
            (r"/product/file-upload",           product_handler.UploadPictureHandler)
            ]

        settings = dict(
            blog_title      = u"Community",
            template_path   = os.path.join(os.path.dirname(__file__), "templates"),
            static_path     = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies    = True,
            cookie_secret   = "12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url       = "/auth/login",
            autoescape      = None,
            debug           = True,
        )

        tornado.web.Application.__init__(self, handlers, **settings) 

        ''' configure database '''
        connection  = pymongo.Connection("localhost", 27017)
        self.db     = connection.market_tab

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
