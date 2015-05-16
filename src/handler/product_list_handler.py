#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from basehandler import BaseHandler
from ..globals import Menu
from ..model10.product import Product


class ProductListHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.PRODUCTOS_LISTA)  # change menu active item

        page = self.get_argument("page", 1)
        items = self.get_argument("items", 30)
        dn = self.get_argument("dn", "")
        message = self.get_argument("message", "")

        product = Product()
        product_list = []

        res_list = product.GetList(page, items)

        if "success" in res_list:
            product_list = res_list["success"]

        total_pages = 0

        res_total_pages = product.GetListTotalPages(items)

        if "success" in res_total_pages:
            total_pages = res_total_pages["success"]

        # print total_pages

        self.render("product/list.html", 
                    dn=dn, 
                    side_menu=self.side_menu,
                    product_list=product_list,
                    page=page,
                    message = message,
                    total_pages=float(total_pages))
