#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model10.webpay import Webpay
from bson import json_util
from base_handler import BaseHandler


class InitByOrderIdHandler(BaseHandler):

    def post(self):
        # validate access token
        if not self.ValidateToken():
            return

        order_id = self.get_argument("order_id","")

        if order_id != "":

            webpay = Webpay()
            res = webpay.InitByOrderId(order_id)

            self.write(json_util.dumps(res))

        else:

            self.write(json_util.dumps({"error":"invalid order id"}))