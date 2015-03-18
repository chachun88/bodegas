#!/usr/bin/env python

from model10.size import Size

from base_handler import BaseHandler
from bson import json_util


class ListHandler(BaseHandler):

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        size = Size()
        self.write(json_util.dumps(size.list()))


class InitByNameHandler(BaseHandler):

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        size = Size()
        size.name = self.get_argument("name", "")
        self.write(json_util.dumps(size.initByName()))
