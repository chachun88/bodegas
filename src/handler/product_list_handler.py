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
from bson import json_util


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
                    total_pages=float(total_pages),
                    dumps=json_util.dumps)

    @tornado.web.authenticated
    def post(self):
        start = int(self.get_argument("start", 0))
        items = self.get_argument("items", 20)
        term = self.get_argument("search[value]","")
        query = ""

        if term != "":
            query = """where unaccent(lower(coalesce(p.name, ''))) like '%%(term)s%' or unaccent(lower(coalesce(p.name, ''))) like '%%(term)s%'"""

        columns = [
            ""
            "order_id",
            "o.date",
            "customer",
            "tipo_cliente",
            "source",
            "items_quantity",
            "total",
            "o.state",
            "payment_type"
        ]

        column = int(self.get_argument("order[0][column]"))
        direction = self.get_argument("order[0][dir]")

        page = int(start / items) + 1

        total_items = 0

        if column > 0:
            column -= 1
        else:
            direction = 'desc'

        order = Order()
        pedidos = order.List(page, items, query, columns[column], direction, term)
        res_total_items = order.getTotalItems(query, term)

        if "success" in res_total_items:
            total_items = res_total_items["success"]

        result = {
            "recordsTotal": total_items,
            "recordsFiltered": total_items,
            "data": pedidos
        }

        self.write(json_util.dumps(result))