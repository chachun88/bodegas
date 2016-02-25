#!/usr/bin/python
# -*- coding: UTF-8 -*-


from basehandler import BaseHandler


class DafitiSynchronizedHandler(BaseHandler):

    def get(self, sku):
        self.write({ "synchronized" : True })
