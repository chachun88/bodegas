 #!/usr/bin/env python


from datetime import date
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
# import pymongo

import access_token
import product_handler
import seller_handler
import brand_handler
import order_handler
import order_detail_handler
import cellar_handler
import category_handler
import color_handler
import customer_handler
import contact_handler
import tag_handler
import city_handler
import shipping_handler
import webpay_handler
import size_handler

import doc_handler
from bson.objectid import ObjectId

from tornado.options import define, options

from globals import ws_port, debugMode

define("port", default=ws_port, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/",                      access_token.AccessTokenHandler),
            (r"/access_token",          access_token.AccessTokenHandler),

            (r"/cellar/add",            cellar_handler.CellarAddHandler),
            (r"/cellar/edit",           cellar_handler.CellarAddHandler),
            (r"/cellar/list",           cellar_handler.CellarListHandler),
            (r"/cellar/find",           cellar_handler.CellarFindHandler),
            (r"/cellar/remove",         cellar_handler.CellarRemoveHandler),

            (r"/cellar/products/list",      cellar_handler.CellarProductsListHandler),
            (r"/cellar/products/add",       cellar_handler.CellarProductsAddHandler),
            (r"/cellar/products/remove",    cellar_handler.CellarProductsAddHandler),
            (r"/cellar/products/kardex",    cellar_handler.CellarProductsKardex),
            (r"/cellar/exists",             cellar_handler.CellarExistsHandler),
            (r"/cellar/products/find",      cellar_handler.CellarProductFind),
            (r"/cellar/selectforsale",      cellar_handler.SelectForSaleHandler),
            (r"/cellar/selectreservation",  cellar_handler.SelectReservationHandler),
            (r"/cellar/getwebcellar",       cellar_handler.GetWebCellarHandler),
            (r"/cellar/getreservationcellar",       cellar_handler.GetReservationCellarHandler),
            (r"/cellar/lastkardex",       cellar_handler.LastKardexHandler),
            (r"/cellar/findbyid",       cellar_handler.FindByIdHandler),

            (r"/product/add",           product_handler.AddProductHandler),
            (r"/product/edit",          product_handler.AddProductHandler),
            (r"/product/remove",        product_handler.RemoveProductHandler),
            (r"/product/find",          product_handler.GetProductHandler),
            (r"/product/list",          product_handler.ListProductsHandler),
            (r"/product/search",        product_handler.SearchHandler),
            (r"/product/for_sale",      product_handler.ForSaleHandler),
            (r"/product/checkstock",    product_handler.CheckStockHandler),

            (r"/salesman/add",          seller_handler.AddSellerHandler),
            (r"/salesman/edit",         seller_handler.AddSellerHandler),
            (r"/salesman/remove",       seller_handler.RemoveSellerHandler),
            (r"/salesman/delete",       seller_handler.RemoveSellerHandler), ## old, must be deleted
            (r"/salesman/find",         seller_handler.GetSalesmanHandler),
            (r"/salesman/list",         seller_handler.ListSalesmanHandler),

            (r"/brand/add",             brand_handler.AddBrandHandler),
            (r"/brand/edit",            brand_handler.AddBrandHandler),
            (r"/brand/remove",          brand_handler.RemoveBrandHandler),
            (r"/brand/find",            brand_handler.GetBrandHandler),
            (r"/brand/list",            brand_handler.LisBrandHandler),

            (r"/category/add",             category_handler.AddCategoryHandler),
            (r"/category/edit",            category_handler.AddCategoryHandler),
            (r"/category/remove",          category_handler.RemoveCategoryHandler),
            (r"/category/find",            category_handler.GetCategoryHandler),
            (r"/category/list",            category_handler.LisCategoryHandler),

            (r"/color/add",             color_handler.AddColorHandler),
            (r"/color/edit",            color_handler.AddColorHandler),
            (r"/color/remove",          color_handler.RemoveColorHandler),
            (r"/color/find",            color_handler.GetColorHandler),
            (r"/color/list",            color_handler.LisColorHandler),            

            (r"/order/add",             order_handler.AddOrderHandler),
            (r"/order/edit",            order_handler.EditOrderHandler),
            (r"/order/remove",          order_handler.RemoveOrderHandler),
            (r"/order/find",            order_handler.GetOrderHandler),
            (r"/order/list",            order_handler.ListOrderHandler),
            (r"/order/changestate",     order_handler.ChangeStateHandler),
            (r"/order/cancel",          order_handler.CancelHandler),
            (r"/order/totalpages",      order_handler.GetTotalPagesHandler),

            (r"/order-detail/save",     order_detail_handler.AddOrderDetailHandler),
            (r"/order-detail/remove",   order_detail_handler.RemoveOrderDetailHandler),
            (r"/order-detail/find",     order_detail_handler.GetOrderDetailHandler),
            (r"/order-detail/list",     order_detail_handler.ListOrderDetailHandler),
            (r"/order-detail/listbyorderid", order_detail_handler.ListDetailByOrderIdHandler),

            (r"/product/file-upload-sample",    product_handler.UploadPictureSampleHandler),
            (r"/product/file-upload",           product_handler.UploadPictureHandler),

            (r"/doc",                           doc_handler.DocHandler),
            (r"/doc/product",                   doc_handler.DocHandler),
            (r"/doc/cellar",                    doc_handler.DocCellarHandler),
            (r"/doc/brand",                     doc_handler.DocBrandHandler),
            (r"/doc/category",                  doc_handler.DocCategoryHandler),
            (r"/doc/salesman",                  doc_handler.DocSalesmanHandler),

            (r"/customer",                           customer_handler.ListHandler),
            (r"/customer/save",                      customer_handler.SaveHandler),
            (r"/customer/edit",                      customer_handler.EditHandler),
            (r"/customer/changestate",               customer_handler.ChangeStateHandler),
            (r"/customer/remove",                    customer_handler.RemoveHandler),
            (r"/customer/initbyid",                  customer_handler.InitByIdHandler),
            (r"/customer/gettypes",                  customer_handler.GetTypesHandler),
            (r"/customer/gettotalpages",             customer_handler.GetTotalPagesHandler),

            (r"/contact/save",                 contact_handler.SaveHandler),
            (r"/contact/edit",                 contact_handler.EditHandler),
            (r"/contact/listbycustomerid",     contact_handler.ListByCustomerIdHandler),
            (r"/contact/changestate",               contact_handler.ChangeStateHandler),
            (r"/contact/remove",                    contact_handler.RemoveHandler),
            (r"/contact/initbyid",                  contact_handler.InitByIdHandler),
            (r"/contact/gettypes",                  contact_handler.GetTypesHandler),

            (r"/tag/save",                       tag_handler.SaveHandler),
            (r"/tag/addtagproduct",              tag_handler.AddTagProductHandler),
            (r"/tag/list",                       tag_handler.ListHandler),
            (r"/tag/initbyid",                   tag_handler.InitByIdHandler),
            (r"/tag/productsbytagid",            tag_handler.GetProductsByTagIdHandler),
            (r"/tag/removeasociationbytagid",    tag_handler.RemoveTagsAsociationByTagIdHandler),
            (r"/tag/hideshow",                   tag_handler.HideShowHandler),
            (r"/tag/remove",                     tag_handler.RemoveHandler),

            (r"/city/save",                      city_handler.SaveHandler),
            (r"/city/list",                      city_handler.ListHandler),

            (r"/shipping/save",                      shipping_handler.SaveHandler),
            (r"/shipping/list",                      shipping_handler.ListHandler),
            (r"/shipping/action",                    shipping_handler.ActionHandler),
            (r"/shipping/initbyid",                  shipping_handler.InitByIdHandler),
            (r"/shipping/remove",                    shipping_handler.RemoveHandler),
            (r"/shipping/save_tracking",             shipping_handler.SaveTrackingHandler),

            (r"/webpay/initbyorderid",               webpay_handler.InitByOrderIdHandler),

            (r"/size/list",               size_handler.ListHandler),
            (r"/size/initbyname",               size_handler.InitByNameHandler)
            ]

        settings = dict(
            blog_title      = u"Community",
            template_path   = os.path.join(os.path.dirname(__file__), "templates"),
            static_path     = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies    = False,
            cookie_secret   = "12oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url       = "/auth/login",
            autoescape      = None,
            debug           = True,
        )

        tornado.web.Application.__init__(self, handlers, **settings) 

        # ''' configure database '''
        # connection  = pymongo.Connection("localhost", 27017)

        # if debugMode:
        #     self.db = connection.dev_market_tab
        #     print "database : dev_market_tab"
        # else:
        #     self.db = connection.market_tab
        #     print "database : market_tab"


        # ''' repair script for user permissions '''
        # users_list = self.db.salesman.find()
        # for user in users_list:
        #     user_id = user["_id"]

        #     try:
        #         permissions = user["permissions"]
        #     except Exception, e:
        #         ## adding empty permissions

        #         self.db.salesman.update( { "_id": ObjectId(user_id) }, { "$set": { "permissions": [] } } )
        #         print "user updated"

        #         pass

        # product_list = self.db.product.find()
        # for product in product_list:
        #     product_id = product["_id"]

        #     try:
        #         upc = product["upc"]
        #     except Exception, e:
        #         self.db.product.update( { "_id": ObjectId(product_id) }, { "$set": {"upc": ""} })
        #         pass

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
