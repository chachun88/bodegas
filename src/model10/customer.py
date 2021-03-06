#!/usr/bin/python
# -*- coding: UTF-8 -*-

from bson import json_util
from basemodel import BaseModel
from contact import Contact
import psycopg2
import psycopg2.extras
import pytz
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

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select u.*,ut.name as type from "User" u left join "User_Types" ut on ut.id = u.type_id where u.id = %(id)s limit 1'''

        parametros = {
            "id":_id
        }

        try:
            cur.execute(query,parametros)
            if cur.rowcount > 0:
                customer = cur.fetchone()
                try:
                    self.id = customer["id"]
                    self.name = customer["name"]
                    self.lastname = customer["lastname"]
                    self.type = customer["type"]
                    self.rut = customer["rut"]
                    self.bussiness = customer["bussiness"]
                    self.approval_date = customer["approval_date"]
                    self.registration_date = customer["registration_date"]
                    self.status = customer["status"]
                    self.first_view = customer["first_view"]
                    self.last_view = customer["last_view"]
                    self.username = customer["name"]
                    self.password = customer["password"]
                    self.email = customer["email"]
                    return self.ShowSuccessMessage(self)
                except Exception, e:
                    return self.ShowError(str(e))
            else:
                return self.ShowError("customer not found")
        except Exception,e:
            return self.ShowError("error init by id {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

    def Save(self):

        customer = {
            "name": self.name,
            "lastname": self.lastname,
            "type": self.type,
            "rut": self.rut,
            "bussiness": self.bussiness,
            "approval_date": None,
            "status": self.status,
            "username": self.username,
            "password": self.password,
            "email": self.email
        }

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''\
                insert into "User" (name,
                                    lastname,
                                    type_id,
                                    rut,
                                    bussiness,
                                    approval_date,
                                    registration_date,
                                    status,
                                    first_view,
                                    last_view,
                                    password,
                                    email)
                values (%(name)s,
                        %(lastname)s,
                        %(type)s,
                        %(rut)s,
                        %(bussiness)s,
                        %(approval_date)s,
                        localtimestamp,
                        %(status)s,
                        localtimestamp,
                        localtimestamp,
                        %(password)s,
                        %(email)s)
                returning id'''

        try:
            # return self.ShowError(cur.mogrify(query, customer))
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

    def List(self, current_page=1, items_per_page=20, query="", column="u.registration_date", dir='desc', term=''):

        skip = int(items_per_page) * ( int(current_page) - 1 )

        lista = {}

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if current_page == 0 and items_per_page == 0:
            query = '''\
                    select  u.id,
                            u.email,
                            u.name,
                            nullif(u.rut,'') as rut,
                            ut.name as type,
                            nullif(u.bussiness,'') as bussiness,
                            to_char(u.registration_date, 'DD/MM/YY HH12:MI') as registration_date,
                            to_char(u.last_view, 'DD/MM/YY HH12:MI') as last_view,
                            CASE WHEN u.status=1 THEN 'PENDIENTE'
                                WHEN u.status=2 THEN 'ACEPTADO'
                            END as status,
                            coalesce(city.name,'') as city,
                            c.town
                    from "User" u 
                    inner join "User_Types" ut on ut.id = u.type_id 
                    left join (select distinct on(user_id) city_id, id, town, user_id from "Contact") as c on c.user_id = u.id
                    left join "City" city on city.id = c.city_id
                    where (u.type_id = 4 or u.type_id = 3) 
                        and u.email <> '' 
                        and u.deleted = 0 
                        {query}
                    order by {column} {dir} 
                    nulls last'''.format(query=query,column=column,dir=dir)

            parametros = {
                "term": term
            }
        else:
            query = '''\
                    select  u.id,
                            u.email,
                            u.name,
                            nullif(u.rut,'') as rut,
                            ut.name as type,
                            nullif(u.bussiness,'') as bussiness,
                            to_char(u.registration_date, 'DD/MM/YY HH12:MI') as registration_date,
                            to_char(u.last_view, 'DD/MM/YY HH12:MI') as last_view,
                            CASE WHEN u.status=1 THEN 'PENDIENTE'
                                WHEN u.status=2 THEN 'ACEPTADO'
                            END as status,
                            coalesce(city.name,'') as city,
                            c.town
                    from "User" u 
                    inner join "User_Types" ut on ut.id = u.type_id 
                    left join (select distinct on(user_id) city_id, id, town, user_id from "Contact") as c on c.user_id = u.id
                    left join "City" city on city.id = c.city_id
                    where (u.type_id = 4 or u.type_id = 3) 
                        and u.email <> '' 
                        and u.deleted = 0 
                        {query}
                    order by {column} {dir} 
                    nulls last
                    limit %(items)s 
                    offset %(offset)s'''.format(query=query,column=column,dir=dir)

            parametros = {
                "term": term,
                "items": items_per_page,
                "offset": skip
            }

        try:
            cur.execute(query,parametros)
            lista = cur.fetchall()

        except:
            pass

        return lista

    def getTotalPages(self, page, items):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select ceil(count(*)::float/%(items)s::float) as pages 
                from "User" u 
                inner join "User_Types" ut on ut.id = u.type_id 
                left join (select distinct on(user_id) city_id, id, town, user_id from "Contact") as c on c.user_id = u.id
                left join "City" city on city.id = c.city_id
                where (u.type_id = 4 or u.type_id = 3) 
                and u.email <> '' 
                and u.deleted = 0'''

        parameters = {
            "items" : items
        }

        try:
            # print cur.mogrify(query, parameters)
            cur.execute(query, parameters)
            pages = cur.fetchone()["pages"]

            return self.ShowSuccessMessage(pages)

        except Exception, e:

            return self.ShowError(str(e))

    def getTotalItems(self, query="", term=''):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''
                select count(*) as items
                from "User" u 
                inner join "User_Types" ut on ut.id = u.type_id 
                left join (select distinct on(user_id) city_id, id, town, user_id from "Contact") as c on c.user_id = u.id
                left join "City" city on city.id = c.city_id
                where (u.type_id = 4 or u.type_id = 3) 
                    and u.email <> '' 
                    and u.deleted = 0 
                    {query}'''.format(query=query)
        parameters = {
            "term": term
        }

        try:
            cur.execute(query, parameters)
            items = cur.fetchone()["items"]
            return self.ShowSuccessMessage(items)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()

    def ChangeState(self,ids,state):

        results = ids.split(",")

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if int(state) == ESTADO_ACEPTADO:

            try:
                query = '''update "User" set status = %(status)s, approval_date = to_date(%(approval_date)s,'DD-MM-YYYY HH24:MI:SS') where id = ANY(%(ids)s)'''
                parametros = {
                    "ids":map(int, results),
                    "status":int(state),
                    "approval_date":datetime.now(pytz.timezone('Chile/Continental')).strftime('%d-%m-%Y %H:%M:%S')
                }
                # print cur.mogrify(query,parametros)
                cur.execute(query,parametros)
                self.connection.commit()
                return self.ShowSuccessMessage("users {} status has been changed to acepted".format(ids))
            except Exception,e:
                return self.ShowError(str(e))

            # self.collection.update({"id":{"$in":[int(n) for n in ids.split(",")]}},{"$set":{"status":state,"approval_date":datetime.now().strftime('%d-%m-%Y %H:%M:%S')}},multi=True)
        else:
            # self.collection.update({"id":{"$in":[int(n) for n in ids.split(",")]}},{"$set":{"status":state}},multi=True)

            try:
                query = '''update "User" set status = %(status)s where id = ANY(%(ids)s)'''
                parametros = {
                    "ids":map(int, results),
                    "status":int(state)
                }
                # print cur.mogrify(query,parametros)
                cur.execute(query,parametros)
                self.connection.commit()
                return self.ShowSuccessMessage("users {} status has been changed to {}".format(ids,state))
            except Exception,e:
                return self.ShowError(str(e))

    def Remove(self,ids):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = '''delete from "Contact" where user_id = ANY(%(ids)s)'''
            parametros = {
                "ids":[int(n) for n in ids.split(",")]
            }
            cur.execute(query,parametros)

            query = '''delete from "User" where id = ANY(%(ids)s)'''
            parametros = {
                "ids":[int(n) for n in ids.split(",")]
            }
            cur.execute(query,parametros)
            self.connection.commit()
            return self.ShowSuccessMessage("Users has been deleted")
        except Exception,e:
            return self.ShowError(str(e))
        finally:
            cur.close()
            self.connection.close()

    def GetTypes(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "User_Types"'''

        try:
            cur.execute(query)
            tipos = cur.fetchall()
            return self.ShowSuccessMessage(tipos)
        except Exception,e:
            return self.ShowError(str(e))
