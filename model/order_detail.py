#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util
from product import Product

class OrderDetail(BaseModel):

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def order_id(self):
        return self._order_id
    @order_id.setter
    def order_id(self, value):
        self._order_id = value
    
    @property
    def product(self):
        return self._product
    @product.setter
    def product(self, value):
        self._product = value
    
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        self._quantity = value
    
    @property
    def total(self):
        return self._total
    @total.setter
    def total(self, value):
        self._total = value

    @property
    def product_id(self):
        return self._product_id
    @product_id.setter
    def product_id(self, value):
        self._product_id = value
    
    

    def __init__(self):
        BaseModel.__init__(self)
        self._id    = ""
        self._order_id  = ""
        self._quantity  = ""
        self._product = Product()
        self._total     = ""
        self._product_id = ""

    def Save(self):
        url = self.wsurl() + "/order-detail/save"
        url += "?token=" + self.token
        url += "&order_id=" + self.order_id
        url += "&quantity=" + self.quantity
        url += "&total=" + self.total
        url += "&product_id=" + self.product_id

        return urllib.urlopen(url).read()

    def Remove(self):
        url = self.wsurl() + "/order/remove"
        url += "?token=" + self.token
        url += "&id=" + self.identifier

        return urllib.urlopen(url).read()

    def InitWithId(self, idd):
        url = self.wsurl() + "/order-detail/find"
        url += "?token=" + self.token
        url += "&id={}".format(idd)

        json_string = urllib.urlopen(url).read()
        json_data = json_util.loads(json_string)

        # print json_data

        self._id = str(json_data["_id"])
        self._order_id = json_data["order_id"]
        self._quantity = json_data["quantity"]
        self._total = json_data["total"]
        self._product_id = json_data["product_id"]

        product = Product()
        product.InitWithId(self._product_id)
        self._product = product

    def ListByOrderId(self, order_id, page=1, items=20):
        url = self.wsurl() + "/order-detail/listbyorderid"
        url += "?token=" + self.token
        url += "&page={}".format(page)
        url += "&items={}".format(items)
        url += "&order_id={}".format(order_id)

        json_string = urllib.urlopen(url).read()
        
        return json_util.loads(json_string)

    def List(self, page=1, items=20):
        url = self.wsurl() + "/order/list"
        url += "?token=" + self.token
        url += "&page={}".format(page)
        url += "&items={}".format(items)

        json_string = urllib.urlopen(url).read()
        print json_string
        return json_util.loads(json_string)
    
    