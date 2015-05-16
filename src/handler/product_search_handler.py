#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from ..globals import Menu
from ..model10.product import Product
import math
from basehandler import BaseHandler


class ProductSearchHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        
        self.set_active(Menu.PRODUCTOS_LISTA)  # change menu active item

        page = self.get_argument("page", 1)
        items = self.get_argument("items", 30)
        dn = self.get_argument("dn", "")
        message = self.get_argument("message", "")
        query = self.get_argument("q", "")

        product = Product()

        product_list = product.Search(query)

        total_pages = math.ceil(float(len(product_list)/float(items)))

        # self.render("product/list.html", dn="", side_menu=self.side_menu, product_list=product.Search(query))

        self.render("product/list.html", 
                    dn=dn, 
                    side_menu=self.side_menu,
                    product_list=product_list,
                    page=page,
                    message = message,
                    total_pages=float(total_pages))
