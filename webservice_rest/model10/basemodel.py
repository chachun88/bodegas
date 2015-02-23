#!/usr/bin/python
# -*- coding: UTF-8 -*-

import psycopg2
import psycopg2.extras
import math
from bson import json_util
from bson.objectid import ObjectId


class BaseModel(object):
    def __init__(self):

        self._connection = psycopg2.connect("host='localhost' dbname='giani' user='yichun' password='chachun88'")
        self._table = ""
        self._id = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value):
        self._table = value

    @property
    def connection(self):
        if self._connection.closed != 0:
            self._connection = psycopg2.connect("host='ondev.today' dbname='giani' user='yichun' password='chachun88'")

        return self._connection

    def Save(self):
        return ShowError("must be overriden by user")

    def InitById(self, idd):
        return ShowError("must be overriden by user")

    def GetList(self, page, items):

        page = int(page)
        items = int(items)
        offset = (page-1)*items
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute("select * from \"{tabla}\" limit {items} offset {offset}".format(tabla=self.table,items=items,offset=offset))
            lista = cur.fetchall()
            return lista
        except Exception,e:
            print str(e)
            return {}

        # return self.collection.find().skip((page-1)*items).limit(items)

    # @return integer
    def GetPages(self, limit):

        items = float(limit)
        cur = self.connection.cursor()
        try:
            cur.execute("select count(*) from \"{tabla}\"".format(tabla=self.table))
            total = float(cur.fetchone()[0])
            paginas = math.floor(total/items)
            return paginas
        except Exception,e:
            print str(e)
            return 0

        # try:
        #   items = int(limit)
        #   items = self.collection.find().count() / items

        #   return items
        # except Exception, e:
        #   return 0

    # @return json object
    def Remove(self):
        try:
            # raise exception if identifier is empty
            if self.id != "":

                cur = self.connection.cursor()
                q = '''delete from "{tabla}" where id = %(id)s'''.format(tabla=self.table)
                p = {
                    "id":self.id
                }
                print cur.mogrify(q,p)
                cur.execute(q,p)
                self.connection.commit()
                return self.ShowSuccessMessage("object: {} has been deleted".format(self.id))
            else:
                return self.ShowError("identifier not found")   
        except Exception, e:
            return self.ShowError("object: not found, error:{}".format(str(e)))

    # @return json object
    def ShowError(self, error_text):
        return {'error': error_text}

    # @return json object
    def ShowSuccessMessage(self, message):
        return {'success': message}

    def GetAccessToken(self,appid=""):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''insert into "Access_Token" (time,appid) values (now(),%(appid)s) returning id'''
        parameters = {"appid":appid}

        try:
            cur.execute(query,parameters)
            _id = cur.fetchone()["id"]
            return self.ShowSuccessMessage("{}".format(_id))
        except Exception,e:
            return self.ShowError(str(e))
        finally:
            cur.close()
            self.connection.close()

    def ValidateToken(self,token=""):

        if token == "":
            return self.ShowError("Token viene vacio")
        else:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = '''select count(1) from "Access_Token" where id = %(token)s'''
            parameters = {"token":token}

            try:
                cur.execute(query,parameters)
                if cur.rowcount > 0:
                    return self.ShowSuccessMessage(True)
                else:
                    return self.ShowError(str(e))
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                cur.close()
                self.connection.close()
