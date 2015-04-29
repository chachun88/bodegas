#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util

class Cellar(BaseModel):

    """ docstring for Cellar """
    def __init__(self):
        BaseModel.__init__(self)
        self._name = ""
        self._description = ""
        self._identifier = ""
        self._city = 0
        pass

    def Save(self):
        url = self.wsurl() + "/cellar/add"
        url += "?token=" + self.token
        url += "&name=" + self.name
        url += "&description=" + self.description
        url += "&city={}".format(self.city)

        return urllib.urlopen(url).read()

    def Remove(self):
        url = self.wsurl() + "/cellar/remove"
        url += "?token=" + self.token
        url += "&id=" + self.identifier

        return urllib.urlopen(url).read()

    def ListProducts(self):

        url = self.wsurl() + "/cellar/products/list"

        url += "?token=" + self.token
        url += "&id=" + self.identifier
        url += "&page=1"
        url += "&items=100"

        json_string = urllib.urlopen(url).read()
        return json_util.loads(json_string)

    def ListKardex(self, day, fromm, until):

        url = self.wsurl() + "/cellar/products/kardex"

        url += "?token=" + self.token
        url += "&page=1"
        url += "&items=1"
        url += "&day=" + day
        url += "&from=" + fromm
        url += "&until=" + until

        json_string = urllib.urlopen(url).read()
        return json_util.loads(json_string) 

    def ProductKardex(self, sku, idd, size):

        url = self.wsurl() + "/cellar/products/find"

        # url += "?token=" + self.token
        # url += "&product_sku="+ sku
        # url += "&cellar_id="+ idd
        # url += "&size="+ size

        parameters = {
            "token" : self.token,
            "sku" : sku,
            "cellar_id" : idd,
            "size" : size
        }

        data = urllib.urlencode(parameters)

        json_string = urllib.urlopen(url, data).read()

        return json_util.loads(json_string) 

    def InitWithId(self, idd):
        url = self.wsurl() + "/cellar/find"
        url += "?token=" + self.token
        url += "&id=" + idd

        json_string = urllib.urlopen(url).read()
        json_data = json_util.loads(json_string)

        # print "{}".format(json_string)

        self.identifier = str(json_data["id"])
        self.name = json_data["name"]
        self.description = json_data["description"]

    def InitWithName(self, name):
        url = self.wsurl() + "/cellar/find"
        url += "?token=" + self.token
        url += "&name=" + name

        json_string = urllib.urlopen(url).read()
        json_data = json_util.loads(json_string)

        if "error" not in json_data:

            self.identifier = str(json_data["id"])
            self.name = json_data["name"]
            self.description = json_data["description"]

        return json_data


    def List(self, page, items):
        url = self.wsurl() + "/cellar/list"
        url += "?token=" + self.token
        url += "&page={}".format(page)
        url += "&items={}".format(items)

        json_string = urllib.urlopen(url).read()
        return json_util.loads(json_string)
    
    def AddProducts(self, product_sku, quantity, price, size, color, operation, user):

        url = self.wsurl() + "/cellar/products/add?token=" + self.token

        data = {
            "cellar_id": self.identifier,
            "product_sku": product_sku,
            "operation": operation,
            "quantity": quantity,
            "price": price,
            "size": size,
            "color": color,
            "user": user
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        # print response_str

        return json_util.loads(response_str)

    def RemoveProducts(self, product_sku, quantity, price, size, color, operation, user):
        url = self.wsurl() + "/cellar/products/remove"

        data = {
            "token":self.token,
            "cellar_id": self.identifier,
            "product_sku": product_sku,
            "operation": operation,
            "quantity": quantity,
            "price": price,
            "size": size,
            "color": color,
            "user": user
        }

        post_data = urllib.urlencode(data)

        json_string = urllib.urlopen(url, post_data).read()

        return json_util.loads(json_string)

    def CellarExist( self, cellar_name ):
        url = self.wsurl() + "/cellar/exists?token=" + self.token

        url += "&cellar_name=" + cellar_name

        json_string = urllib.urlopen( url ).read()
        return json_util.loads( json_string )[ "exists" ]

    def SelectForSale(self, cellar_id):

        url = self.wsurl() + "/cellar/selectforsale"

        data = {
        "token":self.token,
        "cellar_id":cellar_id
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def SelectReservation(self, cellar_id):

        url = self.wsurl() + "/cellar/selectreservation"

        data = {
        "token":self.token,
        "cellar_id":cellar_id
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def GetWebCellar(self):

        url = self.wsurl() + "/cellar/getwebcellar"

        data = {
        "token":self.token
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def GetReservationCellar(self):

        url = self.wsurl() + "/cellar/getreservationcellar"

        data = {
            "token":self.token
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def GetLastKardex(self, product_sku, cellar_identifier, size_id):

        url = self.wsurl() + "/cellar/lastkardex"

        data = {
            "token":self.token,
            "product_sku": product_sku,
            "cellar_identifier": cellar_identifier,
            "size_id": size_id
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj
 
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value
    
    @property
    def identifier(self):
        return self._identifier
    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def city(self):
        return self._city
    @city.setter
    def city(self, value):
        self._city = value

    @property
    def for_sale(self):
        return self._for_sale
    @for_sale.setter
    def for_sale(self, value):
        self._for_sale = value
    
    
    