#!/usr/bin/python
# -*- coding: UTF-8 -*-


import tornado
from basehandler import BaseHandler
from src.model10.dafitimodel import DafitiModel


class DafitiSynchronizedHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, sku):

        d = DafitiModel()

        self.write({ "synchronized" : d.ProductExist(sku) })


class DafitiEnableProductHandler(BaseHandler):

    @tornado.gen.coroutine
    def post(self, sku):

        categories = self.get_argument('categories', '')
        main_category = self.get_argument('main_category', '')
        color = self.get_argument('color', '')
        season = self.get_argument('season', '')

        if categories == '' or main_category == '' \
            or season == '' or color == '': 
            return

        d = DafitiModel()
        d.AddProduct(sku, main_category, categories, color, season)


class DafitiDisableProductHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, sku):
        d = DafitiModel()
        d.RemoveProduct(sku)


class DafitiGetCategoriesHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        d = DafitiModel()
        self.write(d.GetCategories()["Categories"]["Category"][0]["Children"] \
            ["Category"][0]["Children"])
