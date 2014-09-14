#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel
from order_detail import OrderDetail
import psycopg2
import psycopg2.extras


class Order(BaseModel):

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
        BaseModel.__init__(self)
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

    def GetOrderById(self, _id):

        # order = self.collection.find_one({"id":int(_id)})

        # if order:
        #     return json_util.dumps(order)
        # else:
        #     return "{}"

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Order" where id = %(id)s limit 1'''

        parametros = {
        "id":_id
        }

        cur.execute(query,parametros)

        order = cur.fetchone()

        if order:
            return order
        else:
            return {}

    def Save(self):

        new_id = db.seq.find_and_modify(query={'seq_name':'order_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]
        
        # validate contrains
        object_id = self.collection.insert({
            "id": new_id,
            "date": self.date,
            "source": self.source,
            "country": self.country,
            "items_quantity": self.items_quantity,
            "product_quantity": self.product_quantity,
            "state": self.state,
            "salesman" : self.salesman,
            "customer" : self.customer,
            "subtotal" : self.subtotal,
            "discount" : self.discount,
            "tax" : self.tax,
            "total" : self.total,
            "address" : self.address,
            "town" : self.town,
            "city" : self.city,
            "type" : self.type
            })

        return str(object_id)

    def DeleteOrders(self,ids):
        self.collection.remove({"id":{"$in":ids}})
        od = OrderDetail()
        for i in ids:
            od.Remove(i)

    def ChangeStateOrders(self,ids,state):
        print ids
        self.collection.update({"id":{"$in":ids}},{"$set":{"state":state}},multi=True)
        