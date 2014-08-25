#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib

from model.base_model import BaseModel
from bson import json_util
from contact import Contact

class Customer(BaseModel):

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
    def lastname(self):
        return self._lastname
    @lastname.setter
    def lastname(self, value):
        self._lastname = value

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def rut(self):
        return self._rut
    @rut.setter
    def rut(self, value):
        self._rut = value

    @property
    def contact(self):
        return self._contact
    @contact.setter
    def contact(self, value):
        self._contact = value
    
    @property
    def bussiness(self):
        return self._bussiness
    @bussiness.setter
    def bussiness(self, value):
        self._bussiness = value
    
    @property
    def approval_date(self):
        return self._approval_date
    @approval_date.setter
    def approval_date(self, value):
        self._approval_date = value

    @property
    def registration_date(self):
        return self._registration_date
    @registration_date.setter
    def registration_date(self, value):
        self._registration_date = value
    
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value

    @property
    def first_view(self):
        return self._first_view
    @first_view.setter
    def first_view(self, value):
        self._first_view = value

    @property
    def last_view(self):
        return self._last_view
    @last_view.setter
    def last_view(self, value):
        self._last_view = value
    
    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, value):
        self._username = value
    
    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        self._password = value
    

    def __init__(self):
        self._id = ""
        self._name = ""
        self._lastname = ""
        self._type = ""
        self._rut = ""
        self._contact = Contact()
        self._bussiness = ""
        self._approval_date = ""
        self._registration_date = ""
        self._status = ""
        self._first_view = ""
        self._last_view = ""
        self._username = ""
        self._password = ""

    def Save(self):

        url = self.wsurl() + "/customer/save"

        data = {
        "token":self.token(),
        "customer_name":self.name,
        "customer_type":self.type,
        "rut":self.rut,
        "lastname":self.lastname,
        "bussiness":self.bussiness,
        "registration_date":self.registration_date,
        "approval_date":self.approval_date,
        "status":self.status,
        "first_view":self.first_view,
        "last_view":self.last_view,
        "contact":self.contact,
        "username":self.username,
        "password":self.password
        }


        post_data = urllib.urlencode(data)

        return urllib.urlopen(url, post_data).read()


    def Remove(self, _id):
        url = self.wsurl() + "/customer/remove"
        data = {
        "token":self.token(),
        "ids":_id
        }

        post_data = urllib.urlencode(data)
        json_string = urllib.urlopen(url, post_data).read()

        print json_string

    def InitWithId(self, idd):
        pass


    def List(self, page=1, items=20):

        url = self.wsurl() + "/customer"

        data = {
        "token":self.token(),
        "page":page,
        "items":items
        }

        post_data = urllib.urlencode(data)
        json_string = urllib.urlopen(url, post_data).read()

        # print json_string

        return json_util.loads(json_string)

    def ChangeState(self,ids,state):

        url = self.wsurl() + "/customer/changestate"

        data = {
        "token":self.token(),
        "ids":ids,
        "state":state
        }

        post_data = urllib.urlencode(data)
        urllib.urlopen(url, post_data).read()

        