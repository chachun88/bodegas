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

        dn = self.get_argument("dn", "")
        message = self.get_argument("message", "")

        pjax = bool(self.get_argument("_pjax", False))

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'
        self.render("product{}/list.html".format(pjax_str), 
                    dn=dn, 
                    side_menu=self.side_menu)

    @tornado.web.authenticated
    def post(self):

        start = int(self.get_argument("start", 0))

        items = int(self.get_argument("length", 20))

        if items == -1:
            items = 0

        term = self.get_argument("search[value]","")

        query = ""

        if term != "":
            query = """\
                    and unaccent(lower(coalesce(p.name, ''))) like %(term)s"""

        columns = [
            "p.for_sale",
            "p.image",
            "p.name",
            "p.size",
            "p.sell_price",
            "p.promotion_price",
            "p.bulk_price",
            "nullif(p.position, 0)"
        ]

        column = int(self.get_argument("order[0][column]"))
        direction = self.get_argument("order[0][dir]")

        try:
            page = int(start / items) + 1
        except:
            page = 0

        total_items = 0

        # if column == 0:
        #     direction = 'desc'

        product = Product()
        pedidos = product.GetList(page, items, query, columns[column], direction, "%{}%".format(term))
        res_total_items = product.getTotalItems(query, "%{}%".format(term))

        if "success" in res_total_items:
            total_items = res_total_items["success"]

        if "success" in pedidos:
            result = {
                "recordsTotal": total_items,
                "recordsFiltered": total_items,
                "data": pedidos["success"]
            }
        else:
            result = {
                "recordsTotal": 0,
                "recordsFiltered": 0,
                "data": {}
            }
        self.write(json_util.dumps(result))
