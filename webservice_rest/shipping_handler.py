#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from model10.shipping import Shipping
from model10.cellar import Cellar
from model10.product import Product
from model10.kardex import Kardex
from model10.order_detail import OrderDetail
from model10.size import Size
import pytz
from base_handler import BaseHandler
from bson import json_util

import datetime

class SaveHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            self.write(json_util.dumps({"error":"invalid token"}))

        shipping = Shipping()
        shipping.identifier = int(self.get_argument("identifier",0))
        shipping.from_city_id = self.get_argument("from_city_id",0)
        shipping.to_city_id = self.get_argument("to_city_id",0)
        shipping.correos_price = self.get_argument("correos_price",0)
        shipping.chilexpress_price = self.get_argument("chilexpress_price",0)
        shipping.price = self.get_argument("price",0)
        shipping.charge_type = self.get_argument("charge_type",1)

        if shipping.identifier == 0:
            shipping.edited = False
        else:
            shipping.edited = True
            
        self.write(json_util.dumps(shipping.Save()))


class ListHandler(BaseHandler):
    
    def post(self):

        if not self.ValidateToken():
            self.write(json_util.dumps({"error":"invalid token"}))

        shipping = Shipping()
        self.write(json_util.dumps(shipping.List()))

class ActionHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            self.write(json_util.dumps({"error":"invalid token"}))

        action = self.get_argument("action","")

        shipping = Shipping()
        self.write(json_util.dumps(shipping.Action(action)))
    
class InitByIdHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            self.write(json_util.dumps({"error":"invalid token"}))

        identifier = int(self.get_argument("identifier",0))

        shipping = Shipping()
        shipping.identifier = identifier

        if identifier == 0:
            self.write(json_util.dumps({"error":"Debe especificar identificador"}))
        else:
            self.write(json_util.dumps(shipping.InitById()))

class RemoveHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            self.write(json_util.dumps({"error":"invalid token"}))

        identifier = int(self.get_argument("identifier",0))

        shipping = Shipping()
        shipping.identifier = identifier


        if identifier == 0:
            self.write(json_util.dumps({"error":"Debe especificar identificador"}))
        else:
            self.write(json_util.dumps(shipping.Remove()))

class SaveTrackingHandler(BaseHandler):

    def post(self):

        if not self.ValidateToken():
            self.write(json_util.dumps({"error":"invalid token"}))

        else:

            order_id = self.get_argument("order_id","")
            tracking_code = self.get_argument("tracking_code","")
            provider_id = self.get_argument("provider_id","")
            new_cellar_id = self.get_argument("new_cellar_id","")

            c = Cellar()
            res_reservation = c.GetReservationCellar()
            if "success" in res_reservation:
                new_cellar_id = res_reservation["success"]

            if order_id == "":
                self.write(json_util.dumps({"error":"invalid order_id"}))
            elif tracking_code == "":
                self.write(json_util.dumps({"error":"invalid tracking_code"}))
            elif provider_id == "":
                self.write(json_util.dumps({"error":"invalid provider_id"}))
            else:

                cellar = Cellar()

                order_detail = OrderDetail()
                details_res = order_detail.ListByOrderId(order_id)

                if "success" in details_res:
                    details = details_res["success"]

                for detail in details:

                    sku = detail["sku"]
                    quantity = detail["quantity"]
                    operation = Kardex.OPERATION_SELL
                    sell_price = detail["price"]
                        
                    _size = Size()
                    _size.name = detail["size"]
                    res_name = _size.initByName()

                    if "success" in res_name:
                        size = _size.id
                    else:
                        print res_name["error"]

                    color = detail["color"]
                    user = 'Sistema - Despacho'

                    k = Kardex()
                    find_kardex = k.FindKardex(sku, new_cellar_id, size)

                    balance_price = 0
                    units = 0

                    if "success" in find_kardex:
                        balance_price = k.balance_price
                        units = k.balance_units

                    if int(units) >= int(quantity): 

                        kardex = Kardex()

                        kardex.product_sku = sku
                        kardex.cellar_identifier = new_cellar_id
                        kardex.date = str(datetime.datetime.now(pytz.timezone('Chile/Continental')).isoformat())

                        kardex.operation_type = operation
                        kardex.units = quantity
                        kardex.price = balance_price
                        kardex.size_id = size
                        kardex.sell_price = sell_price

                        kardex.color= color
                        kardex.user = user

                        response_kardex = kardex.Insert()

                        if "error" in response_kardex:
                            self.write(json_util.dumps(response_kardex))
                            return
                                

                    else:
                        self.write(json_util.dumps({"error":"Stock insuficiente para realizar el movimiento"}))
                        return


                shipping = Shipping()
                res = shipping.SaveTrackingCode(order_id,tracking_code,provider_id)
                self.write(json_util.dumps(res))