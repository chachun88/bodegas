#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util
from bson.objectid import ObjectId
from basemodel import BaseModel
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

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        self._email = value
    

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
        self._email = ""
    
    def InitById(self, _id):

        # customer = self.collection.find_one({"id":int(_id)})

        # if customer:

        #     return customer

        # else:

        #     return {}

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select u.*,ut.name as type from "User" u left join "User_Types" ut on ut.id = u.type_id where u.id = %(id)s limit 1'''

        parametros = {
        "id":_id
        }

        try:
            cur.execute(query,parametros)
            customer = cur.fetchone()
            return self.ShowSuccessMessage(customer)
        except Exception,e:
            return self.ShowError(str(e))

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
        "password": self.password,
        "email": self.email
        }

        # try:

        #     self.collection.insert(customer)

        #     return str(new_id)

        # except Exception, e:

        #     return str(e)

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''insert into "User" (name,lastname,type,rut,bussiness,approval_date,registration_date,status,first_view,last_view,username,password, email)
        values (%(name)s,%(lastname)s,%(type)s,%(rut)s,%(bussiness)s,%(approval_date)s,%(registration_date)s,%(status)s,%(first_view)s,%(last_view)s,%(username)s,%(password)s,%(email)s)
         returning id'''

        try:
            cur.execute(query,customer)
            self.connection.commit()
            customer_id = cur.fetchone()[0]
            return self.ShowSuccessMessage(customer_id)
        except Exception,e:
            return self.ShowError(str(e))

    def Edit(self):

        customer = {
        "name": self.name,
        "lastname": self.lastname,
        "type": self.type,
        "bussiness": self.bussiness,
        "id":self.id,
        "email":self.email
        }

        # try:

        #     self.collection.update({"id":int(self.id)},{"$set":customer})

        #     return str(self.id)

        # except Exception, e:

        #     return str(e)

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''update "User" set name = %(name)s, lastname = %(lastname)s, type_id = %(type)s, bussiness = %(bussiness)s, email = %(email)s where id = %(id)s'''

        try:
            cur.execute(query,customer)
            self.connection.commit()
            
            return self.ShowSuccessMessage(self.id)

        except Exception,e:
            return self.ShowError(str(e))

    def List(self, current_page=1, items_per_page=20):

        skip = int(items_per_page) * ( int(current_page) - 1 )

        #lista = self.collection.find().skip(skip).limit(int(items_per_page))

        lista = {}

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = '''select u.*,ut.name as type from "User" u 
            left join "User_Types" ut on ut.id = u.type_id where (u.type_id = 4 or u.type_id = 3) 
            and u.email <> '' 
            and u.deleted = 0 
            order by id desc
            limit %(limit)s offset %(offset)s'''
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
        
        results = ids.split(",")

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if int(state) == ESTADO_ACEPTADO:

            try:
                query = '''update "User" set status = %(status)s, approval_date = to_date(%(approval_date)s,'DD-MM-YYYY HH24:MI:SS') where id = ANY(%(ids)s)'''
                parametros = {
                "ids":map(int, results),
                "status":int(state),
                "approval_date":datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                }
                print cur.mogrify(query,parametros)
                cur.execute(query,parametros)
                self.connection.commit()
                return self.ShowSuccessMessage("users {} status has been changed to acepted".format(ids))
            except Exception,e:
                return self.ShowError(str(e))
            
            #self.collection.update({"id":{"$in":[int(n) for n in ids.split(",")]}},{"$set":{"status":state,"approval_date":datetime.now().strftime('%d-%m-%Y %H:%M:%S')}},multi=True)
        else:
            # self.collection.update({"id":{"$in":[int(n) for n in ids.split(",")]}},{"$set":{"status":state}},multi=True)

            try:
                query = '''update "User" set status = %(status)s where id = ANY(%(ids)s)'''
                parametros = {
                "ids":map(int, results),
                "status":int(state)
                }
                print cur.mogrify(query,parametros)
                cur.execute(query,parametros)
                self.connection.commit()
                return self.ShowSuccessMessage("users {} status has been changed to {}".format(ids,state))
            except Exception,e:
                return self.ShowError(str(e))

    def Remove(self,ids):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = '''update "User" set deleted = 1 where id = ANY(%(ids)s)'''
            parametros = {
            "ids":[int(n) for n in ids.split(",")]
            }
            cur.execute(query,parametros)
            self.connection.commit()
            return self.ShowSuccessMessage("ok")
        except Exception,e:
            return self.ShowError(str(e))

    def GetTypes(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "User_Types"'''

        try:
            cur.execute(query)
            tipos = cur.fetchall()
            return self.ShowSuccessMessage(tipos)
        except Exception,e:
            return self.ShowError(str(e))