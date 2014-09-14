#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel, db
from contact import Contact
import psycopg2
import psycopg2.extras

from datetime import datetime

ESTADO_PENDIENTE = 1
ESTADO_ACEPTADO = 2

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
        BaseModel.__init__(self)
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

        # customer = self.collection.find_one({"id":int(_id)})

        # if customer:

        #     return customer

        # else:

        #     return {}

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Customer" where id = %(id)s limit 1'''

        parametros = {
        "id":_id
        }

        try:
            cur.execute(query,parametros)
            customer = cur.fetchone()
            return customer
        except:
            return ""

    def Save(self):

        # new_id = db.seq.find_and_modify(query={'seq_name':'customer_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]

        # print self.contact

        customer = {
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

        # try:

        #     self.collection.insert(customer)

        #     return str(new_id)

        # except Exception, e:

        #     return str(e)

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''insert into "Customer" (name,lastname,type,rut,bussiness,approval_date,registration_date,status,first_view,last_view,username,password)
        values (%(name)s,%(lastname)s,%(type)s,%(rut)s,%(bussiness)s,%(approval_date)s,%(registration_date)s,%(status)s,%(first_view)s,%(last_view)s,%(username)s,%(password)s)
         returning id'''

        try:
            cur.execute(query,customer)
            self.connection.commit()
            customer_id = cur.fetchone()[0]
            return customer_id
        except:
            return ""

    def Edit(self):

        customer = {
        "name": self.name,
        "lastname": self.lastname,
        "type": self.type,
        "bussiness": self.bussiness,
        "id":self.id
        }

        # try:

        #     self.collection.update({"id":int(self.id)},{"$set":customer})

        #     return str(self.id)

        # except Exception, e:

        #     return str(e)

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''update "Customer" set name = %(name)s and lastname = %(lastname)s and type = %(type)s and bussiness = %(bussiness)s where id = %(id)s'''

        try:
            cur.execute(query,customer)
            self.connection.commit()
            
            return self.id

        except:
            return ""

    def List(self, current_page=1, items_per_page=20):

        skip = int(items_per_page) * ( int(current_page) - 1 )

        #lista = self.collection.find().skip(skip).limit(int(items_per_page))

        lista = {}

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = '''select * from "Customer" limit %(limit)s offset %(offset)s'''
            parametros = {
            "limit":items_per_page,
            "offset":skip
            }
            cur.execute(query,parametros)
            lista = cur.fetchall()

        except:
            pass

        return lista

    def ChangeState(self,ids,state):
        print ids.split(",")
        if int(state) == ESTADO_ACEPTADO:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            try:
                query = '''update "Customer" set status = %(status)s and approval_date = %(approval_date)s where id in %(ids)s'''
                parametros = {
                "ids":ids.split(","),
                "status":state,
                "approval_date":datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                }
                cur.execute(query,parametros)
                self.connection.commit()

            except:
                pass
            
            #self.collection.update({"id":{"$in":[int(n) for n in ids.split(",")]}},{"$set":{"status":state,"approval_date":datetime.now().strftime('%d-%m-%Y %H:%M:%S')}},multi=True)
        else:
            # self.collection.update({"id":{"$in":[int(n) for n in ids.split(",")]}},{"$set":{"status":state}},multi=True)

            try:
                query = '''update "Customer" set status = %(status)s where id in %(ids)s'''
                parametros = {
                "ids":ids.split(","),
                "status":state
                }
                cur.execute(query,parametros)
                self.connection.commit()

            except:
                pass

    def Remove(self,ids):
        print ids
        # self.collection.remove({"id":{"$in":[int(n) for n in ids.split(",")]}})

        try:
            query = '''delete from "Customer" where id in %(ids)s'''
            parametros = {
            "ids":[int(n) for n in ids.split(",")]
            }
            cur.execute(query,parametros)
            self.connection.commit()

        except:
            pass