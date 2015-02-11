#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model.base_model import BaseModel
from bson import json_util
import urllib

class Shipping(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._identifier = 0
        self._to_city_id = 0
        self._from_city_id = 0
        self._edited = 0
        self._price = 0
        self._correos_price = 0
        self._chilexpress_price = 0
        self._charge_type = 1

    @property
    def identifier(self):
        return self._identifier
    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def from_city_id(self):
        return self._from_city_id
    @from_city_id.setter
    def from_city_id(self, value):
        self._from_city_id = value

    @property
    def to_city_id(self):
        return self._to_city_id
    @to_city_id.setter
    def to_city_id(self, value):
        self._to_city_id = value

    @property
    def correos_price(self):
        return self._correos_price
    @correos_price.setter
    def correos_price(self, value):
        self._correos_price = value

    @property
    def chilexpress_price(self):
        return self._chilexpress_price
    @chilexpress_price.setter
    def chilexpress_price(self, value):
        self._chilexpress_price = value

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        self._price = value
    

    @property
    def edited(self):
        return self._edited
    @edited.setter
    def edited(self, value):
        self._edited = value
    
    @property
    def charge_type(self):
        return self._charge_type
    @charge_type.setter
    def charge_type(self, value):
        self._charge_type = value
    
    
    def Save(self):

        url = self.wsurl() + "/shipping/save"

        data = {
        "token":self.token,
        "from_city_id":self.from_city_id,
        "to_city_id":self.to_city_id,
        "identifier":self.identifier,
        "correos_price":self.correos_price,
        "chilexpress_price":self.chilexpress_price,
        "price":self.price,
        "edited":self.edited,
        "charge_type":self.charge_type
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def List(self):

        url = self.wsurl() + "/shipping/list"

        data = {
        "token":self.token
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj
    
    def Action(self,action):

        url = self.wsurl() + "/shipping/action"

        data = {
        "token":self.token,
        "action":action
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def InitById(self):

        url = self.wsurl() + "/shipping/initbyid"

        data = {
        "token":self.token,
        "identifier":self.identifier
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        if "success" in response_obj:

            data = response_obj["success"]

            self.identifier = data["id"]
            self.from_city_id = data["from_city_id"]
            self.to_city_id = data["to_city_id"]
            self.edited = data["edited"]
            self.correos_price = data["correos_price"]
            self.chilexpress_price = data["chilexpress_price"]
            self.price = data["price"]
            self.charge_type = data["charge_type"]

        return response_obj

    def Remove(self):

        url = self.wsurl() + "/shipping/remove"

        data = {
        "token":self.token,
        "identifier":self.identifier
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj
    
    def SaveTrackingCode(self, order_id, tracking_code, provider_id):

        url = self.wsurl() + "/shipping/save_tracking"

        data = {
        "token":self.token,
        "order_id":order_id,
        "tracking_code":tracking_code,
        "provider_id":provider_id
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        print "sakjdhaskjdhaskjdhasjkdh\n"

        print response_str

        print "\nksajdhsajkdhaskj"

        response_obj = json_util.loads(response_str)

        return response_obj