#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.web
from basehandler import BaseHandler
from ..model10.city import City
from ..model10.shipping import Shipping
from bson import json_util
from emails import TrackingCustomer
import sendgrid
from ..model10.customer import Customer
from ..model10.order import Order
from ..model10.cellar import Cellar
from ..model10.order_detail import OrderDetail
from ..model10.kardex import Kardex
from ..model10.size import Size
import datetime
from lp.globals import enviroment, Enviroment

from ..globals import *

class AddCityHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):

        city = City()
        city.name = self.get_argument("name","").encode("utf-8")
        guardado = city.Save()

        identifier = int(self.get_argument("identifier",0))

        if "success" in guardado:
            if identifier == 0:
                self.redirect("/shipping/save")
            else:
                self.redirect("/shipping/save?identifier={id}".format(id=identifier))
        else:
            self.redirect("/shipping/save?dn=error&mensaje="+guardado["error"])

class SaveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.SHIPPING_SAVE)

        city = City()
        cities = city.List()

        identifier = self.get_argument("identifier","")
        dn = self.get_argument("dn","")
        mensaje = self.get_argument("mensaje","")

        shipping = Shipping()

        if identifier != "":

            shipping.identifier = identifier
            res = shipping.InitById()

            print res

            if "error" in res:
                print res
                self.write(res["error"])


        if "success" in cities:
            self.render("shipping/add.html",cities=cities["success"],shipping=shipping,dn=dn,mensaje=mensaje)
        else:
            self.write(cities["error"])

    @tornado.web.authenticated
    def post(self):

        shipping = Shipping()
        shipping.identifier = self.get_argument("identifier","")
        shipping.from_city_id = self.get_argument("from_city_id",0)
        shipping.to_city_id = self.get_argument("to_city_id",0)
        shipping.correos_price = self.get_argument("correos_price",0)
        shipping.chilexpress_price = self.get_argument("chilexpress_price",0)
        shipping.price = self.get_argument("price",0)
        shipping.edited = bool(self.get_argument("edited", False))
        shipping.charge_type = self.get_argument("charge_type",1)

        guardado = shipping.Save()

        if "success" in guardado:

            if shipping.identifier == "":
                self.redirect("/shipping/list")
            else:
                self.redirect("/shipping/save?identifier={id}".format(id=shipping.identifier))
        else:
            self.write(guardado["error"])


class ListHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.SHIPPING_LIST)

        shipping = Shipping()
        res_lista = shipping.List()
        if "success" in res_lista:
            self.render("shipping/list.html",lista=res_lista["success"])
        else:
            self.write(res_lista["error"])


class ActionHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):

        action = self.get_argument("action","")
        shipping = Shipping()

        if action == "":
            self.write("Debe seleccionar una acción")
        else:
            res = shipping.Action(action)
            if "success" in res:
                self.redirect("/shipping/list")
            else:
                self.write(res["error"])


class RemoveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        identifier = int(self.get_argument("identifier",0))

        if identifier != 0:
            shipping = Shipping()
            shipping.identifier = identifier
            res = shipping.Remove()

            if "success" in res:
                self.redirect("/shipping/list")
            else:
                self.write(res["error"])

        else:

            self.write("Identificador no válido")


class SaveTrackingCodeHandler(BaseHandler):

    def get(self):

        shipping = Shipping()

        resultado = []

        arr_tracking_code = self.get_arguments("tracking_code")

        arr_provider_id = self.get_arguments("provider_id")

        arr_order_id = self.get_arguments("order_id")

        # print arr_order_id

        for x in range(0, len(arr_order_id)):

            order_id = arr_order_id[x]
            tracking_code = arr_tracking_code[x]
            provider_id = arr_provider_id[x]

            provider_name = ""

            o = Order()
            res_order = o.InitWithId(order_id)

            if "success" in res_order:

                if o.state == Order.ESTADO_CANCELADO or (o.state == Order.ESTADO_PENDIENTE and o.payment_type == 2):

                    resultado.append({"error": "el pedido {} esta cancelado o rechazado".format(order_id)})

                else:

                    c = Cellar()
                    res_reservation = c.GetReservationCellar()
                    if "success" in res_reservation:
                        new_cellar_id = res_reservation["success"]

                    if not self.validateEmpty([order_id, tracking_code, provider_id]):

                        order_detail = OrderDetail()
                        details_res = order_detail.ListByOrderId(order_id)

                        if "success" in details_res:
                            details = details_res["success"]
                        else:
                            resultado.append(details_res)
                            break

                        if self.cancelable(details):

                            self.cancel(details)

                            shipping = Shipping()
                            res = shipping.SaveTrackingCode(order_id,tracking_code,provider_id)

                            if "error" in res:
                                resultado.append(res)
                                break
                            else:
                                if int(provider_id) == 1:
                                    provider_name = "Chilexpress"
                                elif int(provider_id) == 2:
                                    provider_name = "Correos de Chile"

                                customer = Customer()
                                response = customer.InitById(res["success"])
                                print response

                                if "success" in response:
                                    TrackingCustomer(customer.email,customer.name,tracking_code,provider_name,order_id)
                        else:
                            resultado.append({"error": "el pedido {} no puede ser despachado, stock es insuficiente".format(order_id)})
                    else:
                        resultado.append({"error":"faltan datos para despachar el pedido {}".format(order_id)})
            else:
                resultado.append(res_order)

        self.write(json_util.dumps(resultado))

    def validateEmpty(self, params = []):

        empty = False

        for param in params:
            if param == '':
                empty = True

        return empty

    def cancelable(self, details):

        cancelable = True

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
                color = detail["color"]
                user = 'Sistema - Despacho'

                k = Kardex()
                find_kardex = k.FindKardex(sku, new_cellar_id, size)

                balance_price = 0
                units = 0

                if "success" in find_kardex:
                    balance_price = k.balance_price
                    units = k.balance_units

                    if int(units) < int(quantity):
                        cancelable = False
                        break
                else:
                    cancelable = False
                    break
            else:
                cancelable = False
                break
        # end for

        return cancelable

    def sendError(self, subject,  msg):
        try:
            if enviroment != Enviroment.LOCAL and enviroment != Enviroment.ONTEST:
                sg = sendgrid.SendGridClient(usuario_sendgrid, pass_sendgrid)
                message = sendgrid.Mail()
                message.set_from(
                    "Bodega Giani <contacto@loadingplay.com>")
                message.add_to(["ricardo@loadingplay.com", "yi@loadingplay.com"])

                message.set_subject(subject)

                message.set_html(msg)
                status, msg = sg.send(message)
            else:
                print msg
        except Exception, ex:
            print str(ex)
            pass

    def cancel(self, details):

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
                        kardex.date = str(datetime.datetime.now().isoformat())
                        kardex.operation_type = operation
                        kardex.units = quantity
                        kardex.price = balance_price
                        kardex.size_id = size
                        kardex.sell_price = sell_price
                        kardex.color = color
                        kardex.user = user

                        response_kardex = kardex.Insert()

                        if "error" in response_kardex:
                            self.sendError("Error marcar despacho, pedido {}"
                                           .format(detail['order_id']), 
                                           response_kardex['error'])
                else:
                    self.sendError("Error al obtener kardex en despacho, pedido {}"
                                           .format(detail['order_id']), 
                                           response_kardex['error'])
            else:
                self.sendError("Error despacho, no encontro talla, pedido {}"
                                           .format(detail['order_id']), 
                                           response_kardex['error'])
