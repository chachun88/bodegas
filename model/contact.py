#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util

class Contact(BaseModel):

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def telephone(self):
        return self._telephone
    @telephone.setter
    def telephone(self, value):
        self._telephone = value
    
    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def customer_id(self):
        return self._customer_id
    @customer_id.setter
    def customer_id(self, value):
        self._customer_id = value

    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, value):
        self._address = value
    
    
    def __init__(self):
        BaseModel.__init__(self)
        self._id = ""
        self._name = ""
        self._email = ""
        self._address = ""
        self._telephone = ""
        self._customer_id = ""
        self._type = ""
        

    def Save(self):

        url = self.wsurl() + "/contact/save"

        data = {
        "token":self.token,
        "name":self.name,
        "email":self.email,
        "address":self.address,
        "telephone":self.telephone,
        "customer_id":self.customer_id,
        "type":self.type
        }

        post_data = urllib.urlencode(data)

        return urllib.urlopen(url, post_data).read()

    def Edit(self):

        url = self.wsurl() + "/contact/edit"

        data = {
        "token":self.token,
        "name":self.name,
        "email":self.email,
        "address":self.address,
        "telephone":self.telephone,
        "customer_id":self.customer_id,
        "type":self.type,
        "id":self.id
        }

        post_data = urllib.urlencode(data)

        return urllib.urlopen(url, post_data).read()

    def ListByCustomerId(self,customer_id):

        url = self.wsurl() + "/contact/listbycustomerid"

        data = {
        "token":self.token,
        "customer_id":customer_id
        }

        post_data = urllib.urlencode(data)

        return urllib.urlopen(url, post_data).read()

    def Remove(self, _id):
        url = self.wsurl() + "/contact/remove"
        data = {
        "token":self.token,
        "ids":_id
        }

        post_data = urllib.urlencode(data)
        json_string = urllib.urlopen(url, post_data).read()

        print json_string

    def ChangeState(self,ids,state):

        url = self.wsurl() + "/contact/changestate"

        data = {
        "token":self.token,
        "ids":ids,
        "state":state
        }

        post_data = urllib.urlencode(data)
        urllib.urlopen(url, post_data).read()

    def InitById(self,_id):

        url = self.wsurl() + "/contact/initbyid"

        data = {
        "token":self.token,
        "id":_id
        }

        post_data = urllib.urlencode(data)
        json_string = urllib.urlopen(url, post_data).read()

        json_obj = json_util.loads(json_string)

        self.id = json_obj["id"]
        self.name = json_obj["name"]
        self.email = json_obj["email"]
        self.address = json_obj["address"]
        self.telephone = json_obj["telephone"]
        self.customer_id = json_obj["customer_id"]
        self.type = json_obj["type"]
        