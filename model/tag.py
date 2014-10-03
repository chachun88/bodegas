#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import urllib2

from basehandler import BaseHandler
from bson import json_util

from model.base_model import BaseModel

class Tag(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._identifier=""
        self._name=""

    @property
    def identifier(self):
        return self._identifier
    @identifier.setter
    def identifier(self, value):
        self._identifier = value
            
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    def Save(self):
        url = self.wsurl() + "/tag/save"
        url += "?token={}".format(self.token)
        url += "&identifier={}".format(self.identifier)
        url += "&name={}".format(name)

        json_obj = urllib.urlopen(url).read()

        return json_util.loads(json_obj)

    def AddTagProduct(self,product_id,tag_id):
        url = self.wsurl() + "/tag/addtagproduct"
        url += "?token={}".format(self.token)
        url += "&product_id={}".format(product_id)
        url += "&tag_id={}".format(tag_id)

        json_obj = urllib.urlopen(url).read()

        return json_util.loads(json_obj)

    def List(self,page,items):

        url = self.wsurl() + "/tag/list?token={}".format(self.token)
        url += "&page={}".format(page)
        url += "&items={}".format(items)

        json_str = urllib.urlopen(url).read()

        return json_util.loads(json_str)

    def InitById(self,identificador):

        url = self.wsurl() + "/tag/initbyid?token={}".format(self.token)
        url += "&id={}".format(identificador)

        json_str = urllib.urlopen(url).read()

        respuesta = json_util.loads(json_str)

        if "success" in respuesta:

            data = respuesta["success"]

            self.identifier = data["id"]
            self.name       = data["name"]

        return respuesta

    def GetProductsByTagId(self,identificador):

        url = self.wsurl() + "/tag/productsbytagid?token={}".format(self.token)
        url += "&id={}".format(identificador)

        json_str = urllib.urlopen(url).read()

        respuesta = json_util.loads(json_str)

        return respuesta