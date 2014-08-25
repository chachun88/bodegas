#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel, db
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
    def registration_date(self):
        return self._registration_date
    @registration_date.setter
    def registration_date(self, value):
        self._registration_date = value
    
    @property
    def approval_date(self):
        return self._approval_date
    @approval_date.setter
    def approval_date(self, value):
        self._approval_date = value

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
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        self._type = value

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
        self.collection = db.customer
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
    
    def InitById(self, _id):

        customer = self.collection.find_one({"id":_id})

        if customer:

            contact = Contact()

            self.id = customer["id"]
            self.name = customer["name"]
            self.lastname = customer["lastname"]
            self.type = customer["type"]
            self.rut = customer["rut"]
            self.contact = contact.List(self.id)
            self.bussiness = customer["bussiness"]
            self.approval_date = customer["approval_date"]
            self.registration_date = customer["registration_date"]
            self.status = customer["status"]
            self.first_view = customer["first_view"]
            self.last_view = customer["last_view"]
            self.username = customer["username"]
            self.password = customer["password"]

            return self

        else:

            return None

    def Save(self):

        new_id = db.seq.find_and_modify(query={'seq_name':'customer_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]

        # print self.contact

        customer = {
        "id": new_id,
        "name": self.name,
        "lastname": self.lastname,
        "type": self.type,
        "rut": self.rut,
        # "contact": self.contact,
        "bussiness": self.bussiness,
        "approval_date": self.approval_date,
        "registration_date": self.registration_date,
        "status": self.status,
        "first_view": self.first_view,
        "last_view": self.last_view,
        "username": self.username,
        "password": self.password
        }

        try:

            self.collection.insert(customer)

            return str(new_id)

        except Exception, e:

            return str(e)

    def Edit(self):

        customer = {
        "id": new_id,
        "name": self.name,
        "lastname": self.lastname,
        "type": self.type,
        "rut": self.rut,
        "bussiness": self.bussiness,
        "approval_date": self.approval_date,
        "registration_date": self.registration_date,
        "status": self.status,
        "first_view": self.first_view,
        "last_view": self.last_view,
        "username": self.username,
        "password": self.password
        }

        try:

            self.collection.update({"id":self.id})

            return new_id

        except Exception, e:

            return str(e)

    def List(self, current_page=1, items_per_page=20):

        skip = int(items_per_page) * ( int(current_page) - 1 )

        lista = self.collection.find().skip(skip).limit(int(items_per_page))

        return lista

    def ChangeState(self,ids,state):
        print ids.split(",")
        self.collection.update({"id":{"$in":[int(n) for n in ids.split(",")]}},{"$set":{"status":state}},multi=True)

    def Remove(self,ids):
        print ids
        self.collection.remove({"id":{"$in":[int(n) for n in ids.split(",")]}})