#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from ..globals import Menu, debugMode

from basehandler import BaseHandler
from ..model10.cellar import Cellar
from ..model10.product import Product
from ..model10.size import Size
from ..model10.kardex import Kardex
from ..model10.order import Order

from bson import json_util
import re


class PjaxHandler(BaseHandler):

    def get(self):

        self.set_active(Menu.BODEGAS_LISTAR)  # change menu active item

        self.render("examples/pjax.html")


class Pjax2Handler(BaseHandler):

    def get(self):

        self.set_active(Menu.BODEGAS_LISTAR)  # change menu active item

        self.render("examples/pjax2.html")