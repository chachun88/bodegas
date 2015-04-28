#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import urllib

from globals import webservice_url, appid

class BaseModel(object):

    def __init__(self):

        url = self.wsurl() + "/?appid={}".format(appid)
        self._token = urllib.urlopen(url).read()

    @property
    def token(self):

        if self._token == "":
            url = self.wsurl() + "/?appid={}".format(appid)
            self._token = urllib.urlopen(url).read()

        return "{}".format(self._token)

    def wsurl(self):
        return webservice_url