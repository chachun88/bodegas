#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util

ACCIONES_ELIMINAR = 1
ACCIONES_ACEPTAR = 2
ACCIONES_DESPACHADO = 3

class Order(BaseModel):

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    

    @property
    def salesman(self):
        return self._salesman
    @salesman.setter
    def salesman(self, value):
        self._salesman = value
        
    @property
    def customer(self):
        return self._customer
    @customer.setter
    def customer(self, value):
        self._customer = value
    
    @property
    def subtotal(self):
        return self._subtotal
    @subtotal.setter
    def subtotal(self, value):
        self._subtotal = value

    @property
    def discount(self):
        return self._discount
    @discount.setter
    def discount(self, value):
        self._discount = value
    
    @property
    def tax(self):
        return self._tax
    @tax.setter
    def tax(self, value):
        self._tax = value
    
    @property
    def total(self):
        return self._total
    @total.setter
    def total(self, value):
        self._total = value
    
    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, value):
        self._address = value
    
    @property
    def town(self):
        return self._town
    @town.setter
    def town(self, value):
        self._town = value
    
    @property
    def city(self):
        return self._city
    @city.setter
    def city(self, value):
        self._city = value

    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, value):
        self._date = value

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def source(self):
        return self._source
    @source.setter
    def source(self, value):
        self._source = value

    @property
    def country(self):
        return self._country
    @country.setter
    def country(self, value):
        self._country = value

    @property
    def items_quantity(self):
        return self._items_quantity
    @items_quantity.setter
    def items_quantity(self, value):
        self._items_quantity = value
    
    @property
    def product_quantity(self):
        return self._product_quantity
    @product_quantity.setter
    def product_quantity(self, value):
        self._product_quantity = value

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value):
        self._state = value

    def __init__(self):
        self._id                     = ""
        self._date                   = ""
        self._type                   = ""
        self._salesman               = ""
        self._customer               = ""
        self._subtotal               = ""
        self._discount               = ""
        self._tax                    = ""
        self._total                  = ""
        self._address                = ""
        self._town                   = ""
        self._city                   = ""
        self._source                 = ""
        self._country                = ""
        self._items_quantity         = ""
        self._product_quantity       = ""
        self._state                  = ""

    def Save(self):
        url = self.wsurl() + "/order/add"
        url += "?token=" + self.token()
        url += "&date=" + self.date.isoformat()
        url += "&type=" + self.type
        url += "&salesman=" + self.salesman
        url += "&customer=" + self.customer
        url += "&subtotal=" + self.subtotal
        url += "&discount=" + self.discount
        url += "&tax=" + self.tax
        url += "&total=" + self.total
        url += "&address=" + self.address
        url += "&town=" + self.town
        url += "&city=" + self.city
        url += "&source=" + self.source
        url += "&country=" + self.country
        url += "&items_quantity=" + self.items_quantity
        url += "&product_quantity" + self.product_quantity
        url += "&state=" + self.state

        url = url.encode("utf-8")

        return urllib.urlopen(url).read()

    def Remove(self, _id):
        url = self.wsurl() + "/order/remove"
        url += "?token=" + self.token()
        url += "&id=" + _id

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

    def ChangeStateOrders(self,ids,state):

        url = self.wsurl() + "/order/changestate"
        url += "?token=" + self.token()
        url += "&ids={}".format(ids)
        url += "&state={}".format(state)

    