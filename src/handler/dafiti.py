#!/usr/bin/python
# -*- coding: UTF-8 -*-


from basehandler import BaseHandler
from src.model10.dafitimodel import DafitiModel


class DafitiSynchronizedHandler(BaseHandler):

    def get(self, sku):

        d = DafitiModel()

        self.write({ "synchronized" : d.ProductExist(sku) })


class DafitiEnableProductHandler(BaseHandler):

    def get(self, sku):
        d = DafitiModel()
        d.AddProduct(sku)


class DafitiDisableProductHandler(BaseHandler):

    def get(self, sku):
        d = DafitiModel()
        d.RemoveProduct(sku)


class DafitiGetCategoriesHandler(BaseHandler):

    def get(self):
        d = DafitiModel()
        self.write(d.GetCategories())
