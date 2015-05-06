#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras
# from bson.objectid import ObjectId

class Brand(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._name = ''

        # self.collection = db.brand
        self.table = 'Brand'

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    def Print(self):
        return {"name":self.name,
                "id":self.id}

    def InitByName(self, name):
        # try:
        #   brands = self.collection.find({"name":name})

        #   if brands.count() >= 1: 
        #       self.name = brands[0]["name"]
        #       self.identifier = str(brands[0]["_id"])
        #   return self.ShowSuccessMessage("brand correctly initialized")
        # except:
        #   return self.ShowError("brand can not be initialized")

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''select * from "Brand" where name = %(name)s'''
        parameters = {
        "name":name
        }
        cur.execute(query,parameters)
        brands = cur.fetchone()
        if brands:
            self.name = brands["name"]
            self.id = brands["id"]
            return self.ShowSuccessMessage("brand correctly initialized")
        else:
            return self.ShowError("brand can not be initialized")

    def InitById(self, idd):
        # try:
        #   brands = self.collection.find({"_id":ObjectId(idd)})

        #   if brands.count() >= 1: 
        #       self.name = brands[0]["name"]
        #       self.identifier = str(brands[0]["_id"])
        #   return self.ShowSuccessMessage("brand correctly initialized")
        # except:
        #   return self.ShowError("brand can not be initialized")

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''select * from "Brand" where id = %(id)s'''
        parameters = {
        "id":idd
        }
        cur.execute(query,parameters)
        brands = cur.fetchone()
        if brands:
            self.name = brands["name"]
            self.id = brands["id"]
            return self.ShowSuccessMessage("brand correctly initialized")
        else:
            return self.ShowError("brand can not be initialized")

    def Save(self):
        # try:
        #   data = self.collection.find({"name":self.name})
        #   if data.count() >= 1:
        #       self.collection.update({
        #           "name":self.name
        #           },{
        #           "$set":{
        #               "name" : self.name,
        #               }
        #           })
        #       self.identifier = str(data[0]["_id"])

        #   else:
        #       self.collection.save({
        #           "name":self.name
        #           })

        #       data = self.collection.find({"name":self.name})
        #       self.identifier = str(data[0]["_id"])

        #   return self.ShowSuccessMessage("brans saved correctly")
        # except:
        #   return self.ShowError("error saving brand")

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''select * from "Brand" where name = %(name)s'''
        parameters = {
        "name":self.name
        }
        cur.execute(query,parameters)
        brands = cur.fetchone()

        if not brands:
            query = '''insert into "Brand" (name) values (%(name)s)'''
            try:
                cur.execute(query,parameters)
                self.connection.commit()
                return self.ShowSuccessMessage("brand saved correctly")
            except Exception,e:
                return self.ShowError("error saving brand: {}".format(str(e)))


    def GetAllBrands(self):
        # return self.collection.find()

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''select * from "Brand"'''
        cur.execute(query)
        brands = cur.fetchall()
        return brands

    def Exist(self, name):
        # if self.collection.find({"name":name}).count() >= 1:
        #   return True
        # return False

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = '''select * from "Brand" where name = %(name)s limit 1'''
        parameters = {
        "name":name
        }
        cur.execute(query,parameters)
        brands = cur.fetchall()
        if brands:
            return True
        else:
            return False