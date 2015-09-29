#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from ..globals import Menu
from basehandler import BaseHandler
from ..model10.cellar import Cellar
from ..model10.product import Product
from ..model10.size import Size


class ReportHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.BODEGAS_LISTAR)  # change menu active item

        pjax = bool(self.get_argument("_pjax", False))

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        _c = Cellar()
        cellars = _c.List(1, 100)

        _p = Product()
        res_list = _p.GetList(0, 0)
        products = []
        if "success" in res_list:
            products = res_list["success"]

        _s = Size()
        res_size = _s.list()
        sizes = []
        if "success" in res_size:
            sizes = res_size["success"]

        sku = self.get_argument("sku", "")
        size_id = self.get_argument("size_id", "")
        cellar_id = self.get_argument("cellar_id", "")

        if sku != "":

            cellar = Cellar()
            cellar.InitById(cellar_id)
            res = cellar.FindProductKardex(sku, cellar_id, size_id, True)

            if "success" in res:
                self.render("report{}/home.html".format(pjax_str), 
                            detail=res["success"], 
                            cellars=cellars, 
                            products=products,
                            sizes=sizes,
                            sku=sku,
                            size_id=size_id,
                            cellar_id=cellar_id)
        else:
            self.render("report{}/home.html".format(pjax_str), 
                        cellars=cellars, 
                        products=products,
                        sizes=sizes,
                        sku=sku,
                        size_id=size_id,
                        cellar_id=cellar_id)
