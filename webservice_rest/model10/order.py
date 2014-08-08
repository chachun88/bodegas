#!/usr/bin/env python

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel, db


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
        self.collection              = db.order
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

    def GetOrderById(self, id):

        order = self.collection.find_one({"id":id})

        return order

    def Save(self):
        
        # validate contrains
        object_id = self.collection.insert({
            "id": self.id,
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
            "city" : self.city 
            })

        return str(object_id)

    def ChangeState(self, id, state):

        try:
            self.collection.update(
                  {"id" : id},
                  {"$set" : {
                      "state" : state
                    }
                  })
            return "ok"
        except Exception, e:
            return str(e)