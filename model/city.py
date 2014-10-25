#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model.base_model import BaseModel
from bson import json_util
import urllib

class City(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._identifier = ""
        self._name = ""

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

        url = self.wsurl() + "/city/save"

        data = {
        "token":self.token,
        "name":self.name,
        "identifier":self.identifier
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def List(self):

        url = self.wsurl() + "/city/list"

        data = {
        "token":self.token
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def Remove(self):

        url = self.wsurl() + "/city/remove"

        data = {
        "token":self.token,
        "name":self.name,
        "identifier":self.identifier
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj


    
    