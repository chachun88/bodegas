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
    def shipping(self):
        return self._shipping
    @shipping.setter
    def shipping(self, value):
        self._shipping = value
    
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

    @property
    def payment_type(self):
        return self._payment_type
    @payment_type.setter
    def payment_type(self, value):
        self._payment_type = value

    @property
    def billing_id(self):
        return self._billing_id
    @billing_id.setter
    def billing_id(self, value):
        self._billing_id = value
    
    @property
    def shipping_id(self):
        return self._shipping_id
    @shipping_id.setter
    def shipping_id(self, value):
        self._shipping_id = value

    @property
    def customer_email(self):
        return self._customer_email
    @customer_email.setter
    def customer_email(self, value):
        self._customer_email = value
    
    

    def __init__(self):
        BaseModel.__init__(self)
        self._id                     = ""
        self._date                   = ""
        self._type                   = ""
        self._salesman               = ""
        self._customer               = ""
        self._subtotal               = ""
        self._shipping               = ""
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
        self._payment_type           = ""
        self._billing_id             = ""
        self._shipping_id            = ""
        self._customer_email         = ""

    def Save(self):
        url = self.wsurl() + "/order/add"
        url += "?token=" + self.token
        url += "&date=" + self.date.isoformat()
        url += "&type=" + self.type
        url += "&salesman=" + self.salesman
        url += "&customer=" + self.customer
        url += "&subtotal=" + self.subtotal
        url += "&shipping=" + self.shipping
        url += "&tax=" + self.tax
        url += "&total=" + self.total
        url += "&address=" + self.address
        url += "&town=" + self.town
        url += "&city=" + self.city
        url += "&source=" + self.source
        url += "&country=" + self.country
        url += "&items_quantity=" + self.items_quantity
        url += "&product_quantity=" + self.product_quantity
        url += "&state=" + self.state
        url += "&payment_type=" + self.payment_type
        url += "&billing_id=" + self.billing_id
        url += "&shipping_id=" + self.shipping_id

        url = url.encode("utf-8")

        return urllib.urlopen(url).read()

    def Remove(self, _id):
        url = self.wsurl() + "/order/remove"
        url += "?token=" + self.token
        url += "&id=" + _id

        response = urllib.urlopen(url).read()

        return json_util.loads(response)

    def InitWithId(self, idd):
        url = self.wsurl() + "/order/find"
        url += "?token=" + self.token
        url += "&id=" + idd

        json_string = urllib.urlopen(url).read()
        json_data = json_util.loads(json_string)

        if "success" in json_data:

            data = json_data["success"]

            self.id                     = data["order_id"]
            self.date                   = data["date"]
            self.type                   = data["type"]
            # self.salesman               = data["salesman"]
            self.customer               = data["customer"]
            self.subtotal               = data["subtotal"]
            self.shipping               = data["shipping"]
            self.tax                    = data["tax"]
            self.total                  = data["total"]
            self.address                = data["address"]
            self.town                   = data["town"]
            self.city                   = data["city"]
            self.source                 = data["source"]
            self.country                = data["country"]
            self.items_quantity         = data["items_quantity"]
            self.product_quantity       = data["products_quantity"]
            self.state                  = data["state"]
            self.payment_type           = data["payment_type"]
            self.billing_id             = data["billing_id"]
            self.shipping_id            = data["shipping_id"]
            self.customer_email         = data["email"]

        return json_data


    def List(self, page=1, items=20):
        url = self.wsurl() + "/order/list"
        url += "?token=" + self.token
        url += "&page={}".format(page)
        url += "&items={}".format(items)

        json_string = urllib.urlopen(url).read()
        # print json_string
        return json_util.loads(json_string)

    def ChangeStateOrders(self,ids,state):

        url = self.wsurl() + "/order/changestate"
        url += "?token=" + self.token
        url += "&ids={}".format(ids)
        url += "&state={}".format(state)
        response = urllib.urlopen(url).read()
        return json_util.loads(response)

    