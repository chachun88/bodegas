#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras
from bson import json_util

class Tag(BaseModel):

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    

    def __init__(self):
        BaseModel.__init__(self)
        self.table = "Tag"

    def Save(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # existe = False

        query = '''select id from "Tag" where name = %(name)s'''
        parameters = {
        "name":self.name
        }

        try:
            cur.execute(query,parameters)

            if cur.rowcount > 0:
                self.id = cur.fetchone()["id"]
            # else:
            #     print "self.id: {}".format(self.id)

        except Exception,e:
            self.connection.close()
            cur.close()
            return self.ShowError("Error al comprobar existencia del tag, {}".format(str(e)))


        if self.id == "":

            query = '''insert into "Tag" (name) values (%(name)s) returning id'''
            parameters = {
            "name":self.name
            }

            try:
                cur.execute(query,parameters)
                self.connection.commit()
                self.id = cur.fetchone()["id"]
                return self.ShowSuccessMessage(self.id)
            except Exception,e:
                return self.ShowError("Error saving tag: {}".format(str(e)))
            finally:
                self.connection.close()
                cur.close()


        else:

            query = '''update "Tag" set name = %(name)s where id = %(id)s returning id'''
            parameters = {
            "name":self.name,
            "id":self.id
            }

            try:
                cur.execute(query,parameters)
                self.id = cur.fetchone()["id"]
                self.connection.commit()
                return self.ShowSuccessMessage(self.id)
            except Exception,e:
                return self.ShowError("Error updating tag: {}".format(str(e)))
            finally:
                self.connection.close()
                cur.close()


    def GetTagsByIds(self,ids):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select * from "Tag" where id = any(%(ids)s)'''
        parameters = {
        "ids":ids
        }

        try:
            cur.execute(query,parameters)
            tags = cur.fetchall()
            return self.ShowSuccessMessage(tags)
        except Exception,e:
            return self.ShowError("Error al buscar tags por id: {}".format(str(e)))
        finally:
            self.connection.close()
            cur.close()

    def GetTagsByProductId(self,_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select * from "Tag" t left join "Tag_Product" tp on tp.tag_id = t.id where tp.product_id = %(id)s'''
        parameters = {
        "id":_id
        }

        try:
            cur.execute(query,parameters)
            tags = cur.fetchall()
            return self.ShowSuccessMessage(tags)
        except Exception,e:
            return self.ShowError("Error al buscar tags por product_id: {}".format(str(e)))
        finally:
            self.connection.close()
            cur.close()

    def AddTagProduct(self,tag_id,product_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select id from "Tag_Product" where tag_id = %(tag_id)s and product_id = %(product_id)s'''
        parameters = {
        "tag_id":tag_id,
        "product_id":product_id
        }

        try:
            cur.execute(query,parameters)

            if cur.rowcount > 0:
                identifier = cur.fetchone()["id"]
                return self.ShowSuccessMessage(str(identifier))
            else:

                query = '''insert into "Tag_Product" (tag_id,product_id) values (%(tag_id)s,%(product_id)s) returning id'''

                try:
                    cur.execute(query,parameters)
                    identifier = cur.fetchone()["id"]
                    self.connection.commit()
                    return self.ShowSuccessMessage(str(identifier))
                except Exception,e:
                    return self.ShowError("Error agregando relacion tag y producto, {}".format(str(e)))
                finally:
                    cur.close()
                    self.connection.close()

        except Exception,e:
            self.connection.close()
            cur.close()
            return self.ShowError("Error al buscar relacion tag y producto, {}".format(str(e)))

        

        



    # def Exists(self,name):

    #   cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    #   query = '''select count(*) cantidad from "Tags" where name = %(name)s'''
    #   parameters = {
    #   "name":name
    #   }

    #   try:
    #       cur.execute(query,parameters)
    #       cantidad = cur.fetchone()["cantidad"]

    #       if cantidad > 0:
    #           return self.ShowSuccessMessage(True)
    #       else:
    #           return self.ShowSuccessMessage(False)

    #   except Exception,e:
    #       return self.ShowError("Error al buscar tags por nombre: {}".format(str(e)))
    #   finally:
    #       self.connection.close()
    #       cur.close()
