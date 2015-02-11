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
    def user_id(self):
        return self._user_id
    @user_id.setter
    def user_id(self, value):
        self._user_id = value
    
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
    def address(self):
        return self._address
    @address.setter
    def address(self, value):
        self._address = value
    
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
    def lastname(self):
        return self._lastname
    @lastname.setter
    def lastname(self, value):
        self._lastname = value

    @property
    def city(self):
        return self._city
    @city.setter
    def city(self, value):
        self._city = value
    
    @property
    def zip_code(self):
        return self._zip_code
    @zip_code.setter
    def zip_code(self, value):
        self._zip_code = value

    @property
    def additional_info(self):
        return self._additional_info
    @additional_info.setter
    def additional_info(self, value):
        self._additional_info = value

    @property
    def town(self):
        return self._town
    @town.setter
    def town(self, value):
        self._town = value
    
    @property
    def rut(self):
        return self._rut
    @rut.setter
    def rut(self, value):
        self._rut = value
    
    
    def __init__(self):
        BaseModel.__init__(self)
        self._id = ""
        self._name = ""
        self._email = ""
        self._address = ""
        self._telephone = ""
        self._user_id = ""
        self._type = ""
        self._lastname = ""
        self._city = ""
        self._zip_code = ""
        self._additional_info = ""
        self._town = ""
        self._rut = ""
        

    def Save(self):

        url = self.wsurl() + "/contact/save"

        data = {
        "token":self.token,
        "name":self.name,
        "email":self.email,
        "address":self.address,
        "telephone":self.telephone,
        "user_id":self.user_id,
        "type_id":self.type,
        "type":self.type,
        "lastname":self.lastname,
        "city":self.city,
        "zip_code":self.zip_code,
        "additional_info":self.additional_info,
        "town":self.town,
        "rut":self.rut
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def Edit(self):

        url = self.wsurl() + "/contact/edit"

        data = {
        "token":self.token,
        "name":self.name,
        "email":self.email,
        "address":self.address,
        "telephone":self.telephone,
        "user_id":self.user_id,
        "type_id":self.type,
        "id":self.id,
        "type":self.type,
        "lastname":self.lastname,
        "city":self.city,
        "zip_code":self.zip_code,
        "additional_info":self.additional_info,
        "town":self.town,
        "rut":self.rut
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def ListByCustomerId(self,user_id):

        url = self.wsurl() + "/contact/listbycustomerid"

        data = {
        "token":self.token,
        "user_id":user_id
        }

        post_data = urllib.urlencode(data)

        response_str =  urllib.urlopen(url, post_data).read()
        response_obj = json_util.loads(response_str)
        return response_obj

    def Remove(self, _id):
        url = self.wsurl() + "/contact/remove"
        data = {
        "token":self.token,
        "ids":_id
        }

        post_data = urllib.urlencode(data)
        json_string = urllib.urlopen(url, post_data).read()

        return json_util.loads(json_string)

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
        self.user_id = json_obj["user_id"]
        self.type = json_obj["type"]
        self.lastname = json_obj["lastname"]
        self.city = json_obj["city"]
        self.zip_code = json_obj["zip_code"]
        self.additional_info = json_obj["additional_info"]
        self.town = json_obj["town"]
        self.rut = json_obj["rut"]

    def GetTypes(self):

        url = self.wsurl() + "/contact/gettypes"

        data = {
        "token":self.token
        }

        post_data = urllib.urlencode(data)

        json_string = urllib.urlopen(url, post_data).read()
        json_obj = json_util.loads(json_string)

        return json_obj

        