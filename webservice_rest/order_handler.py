#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model10.order import Order
from model10.cellar import Cellar
from model10.kardex import Kardex
from model10.order_detail import OrderDetail
from bson import json_util

from base_handler import BaseHandler
import datetime


class ChangeStateHandler(BaseHandler):

    def get(self):
        # validate access token
        if not self.ValidateToken():
            return

        ids = self.get_argument("ids","")
        state = self.get_argument("state","")

        if ids == "":
            self.write("Debe seleccionar al menos un pedido")
            return

        values = ids.split(",")

        _v = []

        for v in values:
            _v.append(int(v))

        order = Order()
        response = order.ChangeStateOrders(_v,state)

        self.write(json_util.dumps(response))


class AddOrderHandler(BaseHandler):  

    def get(self):
        # validate access token
        if not self.ValidateToken():
            return

        # instantiate order
        order = Order()

        order.id                = self.get_argument("id", "")
        order.date              = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        order.salesman          = self.get_argument("salesman", "")
        order.customer          = self.get_argument("customer", "")
        order.subtotal          = self.get_argument("subtotal", "")
        order.discount          = self.get_argument("discount", "")
        order.tax               = self.get_argument("tax", "")
        order.total             = self.get_argument("total", "")
        order.address           = self.get_argument("address", "")
        order.town              = self.get_argument("town", "")
        order.city              = self.get_argument("city", "")
        order.country           = self.get_argument("country","")
        order.type              = self.get_argument("type","")
        order.source            = self.get_argument("source","")
        order.items_quantity    = self.get_argument("items_quantity","")
        order.product_quantity  = self.get_argument("product_quantity","")
        order.state             = self.get_argument("state","")
        order.payment_type      = self.get_argument("payment_type","")
        order.billing_id        = self.get_argument("billing_id","")
        order.shipping_id       = self.get_argument("shipping_id","")

        # saving the current order
        oid = order.Save()

        self.write(oid)


class EditOrderHandler(BaseHandler):
    def get(self):
        # validate access token
        if not self.ValidateToken():
            return

        # instantiate order
        order = Order()

        order.identifier        = self.get_argument("id", "")
        order.salesman          = self.get_argument("salesman_id", "")
        order.customer          = self.get_argument("customer", "")
        order.subtotal          = self.get_argument("subtotal", "")
        order.discount          = self.get_argument("discount", "")
        order.iva               = self.get_argument("iva", "")
        order.total             = self.get_argument("total", "")
        order.address           = self.get_argument("address", "")
        order.town              = self.get_argument("town", "")
        order.city              = self.get_argument("city", "")
        order.country           = self.get_argument("country","")
        order.type              = self.get_argument("type","")
        order.source            = self.get_argument("source","")
        order.items_quantity    = self.get_argument("items_quantity","")
        order.product_quantity  = self.get_argument("product_quantity","")
        order.state             = self.get_argument("state","")
        order.payment_type      = self.get_argument("payment_type","")
        order.billing_id        = self.get_argument("billing_id","")
        order.shipping_id       = self.get_argument("shipping_id","")

        #saving the current order
        oid = order.Edit(self.db.orders)

        self.write(oid)


class RemoveOrderHandler(BaseHandler):
    def get(self):
        #validate constrains
        if not self.ValidateToken():
            return

        order = Order()
        response = order.DeleteOrders(self.get_argument("id", ""))
        self.write(json_util.dumps(response))


class GetOrderHandler(BaseHandler):
    def get(self):
        
        # validate constrains
        if not self.ValidateToken():
            return

        id = self.get_argument("id","")

        order = Order()
        response = order.GetOrderById(id)
        self.write(json_util.dumps(response))


class ListOrderHandler(BaseHandler):
    def get(self):

        # validate constrains
        if not self.ValidateToken():
            return

        order = Order()

        try:
            current_page    = int(self.get_argument("page", "1"))
            items_per_page  = int(self.get_argument("items", "20"))
        except Exception, e:
            print str(e)

        self.write(json_util.dumps(order.GetList(current_page, items_per_page)))
        # self.write(json_util.dumps())


class CancelHandler(BaseHandler):
    """docstring for CancelHandler"""
    
    def post(self):
        
        #validate constrains
        if not self.ValidateToken():
            return

        ids = self.get_argument("ids","")
        cellar_id = None
        web_cellar = None

        cellar = Cellar()
        res_reservation_cellar = cellar.GetReservationCellar()

        if "success" in res_reservation_cellar:
            cellar_id = res_reservation_cellar["success"]
        else:
            self.write(json_util.dumps({"error":res_reservation_cellar["error"]}))

        if ids == "":
            self.write(json_util.dumps({"error":"ids viene vacio"}))
        else:

            identificadores = []

            for identificador in ids.split(","):

                order = Order()
                res_order = order.GetOrderById(identificador)

                cancelable = True

                if "success" in res_order:

                    o = res_order["success"]

                    if o["state"] != Order.ESTADO_CANCELADO:

                        order_detail = OrderDetail()
                        details_res = order_detail.ListByOrderId(identificador)

                        if "success" in details_res:

                            details = details_res["success"]

                            # recorre cada producto del detalle de orden y determina si la orden es cancelable
                            for d in details:

                                k = Kardex()
                                find_kardex = k.FindKardex(d["sku"], cellar_id, d['size_id'])
                                units = 0

                                if "success" in find_kardex:
                                    units = k.balance_units  

                                if int(units) < int(d['quantity']): 

                                    cancelable = False

                            # end for

                            # si no es cancelable la orden se guarda en el array identificadores para avisar al usuario
                            if not cancelable:
                                identificadores.append({"identificador":identificador,"error":"no tiene stock suficiente"})
                            else:

                                cellar = Cellar()
                                res_web_cellar = cellar.GetWebCellar()

                                if "success" in res_web_cellar:

                                    web_cellar = res_web_cellar["success"]

                                # mueve c/u de los productos desde la bodega de reserva a la bodega web
                                kardex = Kardex()
                                res = kardex.moveOrder(details, web_cellar, cellar_id)

                                if "error" in res:
                                    identificadores.append({"identificador":identificador,"error":res["error"]})
                        else:
                            if identificador not in identificadores:
                                identificadores.append({"identificador":identificador,"error":details_res["error"]})
                    elif o["state"] == Order.ESTADO_DESPACHADO:
                        if identificador not in identificadores:
                            identificadores.append(identificadores.append({"identificador":identificador,"error":"Pedido ya esta despachado"}))
                    else:
                        if identificador not in identificadores:
                            identificadores.append(identificadores.append({"identificador":identificador,"error":"Pedido ya esta cancelado"}))
                else:
                    if identificador not in identificadores:
                        identificadores.append(identificadores.append({"identificador":identificador,"error":res_order["error"]}))

            if len(identificadores) > 0:
                self.write(json_util.dumps({"error":identificadores}))
            else:
                self.write(json_util.dumps({"success":"ok"}))


class GetTotalPagesHandler(BaseHandler):
    """ get total pages with items """

    def post(self):

        items = self.get_argument("items", 20)

        order = Order()
        total = order.getTotalPages(items)

        self.write(json_util.dumps(total))