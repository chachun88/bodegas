#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model10.base_model import BaseModel
from bson import json_util
import urllib


class Size(BaseModel):

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

    def list(self):

        url = self.wsurl() + "/size/list"

        data = {
            "token": self.token,
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj

    def initByName(self):

        url = self.wsurl() + "/size/initbyname"

        data = {
            "token" : self.token,
            "name" : self.name
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        if "success" in response_obj:

            self.identifier = response_obj["success"]["id"]
            self.name = response_obj["success"]["name"]

        return response_obj
