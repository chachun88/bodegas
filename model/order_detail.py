#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util

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
    def product_id(self):
        return self._product_id
    @product_id.setter
    def product_id(self, value):
        self._product_id = value
    
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
    

    def __init__(self):
        self._id    = ""
        self._order_id  = ""
        self._quantity  = ""
        self._product_id = ""
        self._total     = ""

    def Save(self):
        url = self.wsurl() + "/order-detail/save"
        url += "?token=" + self.token()
        url += "&id_order=" + self.id_order
        url += "&quantity=" + self.quantity
        url += "&total=" + self.total
        url += "&product_id" + self.product_id

        return urllib.urlopen(url).read()

    def Remove(self):
        url = self.wsurl() + "/order/remove"
        url += "?token=" + self.token()
        url += "&id=" + self.identifier

        return urllib.urlopen(url).read()

    def InitWithId(self, idd):
        url = self.wsurl() + "/order/find"
        url += "?token=" + self.token()
        url += "&id=" + idd

        json_string = urllib.urlopen(url).read()
        json_data = json_util.loads(json_string)

        self._id                     = json_data["id"]
        self._date                   = json_data["date"]
        self._type                   = json_data["type"]
        self._salesman               = json_data["salesman"]
        self._customer               = json_data["customer"]
        self._subtotal               = json_data["subtotal"]
        self._discount               = json_data["discount"]
        self._tax                    = json_data["tax"]
        self._total                  = json_data["total"]
        self._address                = json_data["address"]
        self._town                   = json_data["town"]
        self._city                   = json_data["city"]
        self._source                 = json_data["source"]
        self._country                = json_data["country"]
        self._items_quantity         = json_data["items_quantity"]
        self._product_quantity       = json_data["product_quantity"]
        self._state                  = json_data["state"]


    def List(self, page=1, items=20):
        url = self.wsurl() + "/order/list"
        url += "?token=" + self.token()
        url += "&page={}".format(page)
        url += "&items={}".format(items)

        json_string = urllib.urlopen(url).read()
        print json_string
        return json_util.loads(json_string)
    
    