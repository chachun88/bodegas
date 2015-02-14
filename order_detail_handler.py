#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler
from model.order_detail import OrderDetail
from model.order import Order
from model.product import Product
from model.webpay import Webpay

from bson import json_util

class ListOrderDetailHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        order_id = self.get_argument("order_id","")

        od_list = []

        order = Order()
        response = order.InitWithId(order_id)

        order_detail = OrderDetail()
        
        product = Product()

        webpay_data = {}

        if "error" in response:
            self.render("order_detail/list.html",dn=response["error"],order_detail=od_list,order=order, webpay_data=webpay_data)
        elif order.payment_type == 2:

            webpay = Webpay()
            res_webpay = webpay.InitByOrderId(order_id)

            if "success" in res_webpay:

                res_webpay_data = res_webpay["success"]


                TBK_ORDEN_COMPRA = res_webpay_data["TBK_ORDEN_COMPRA"]
                TBK_MONTO = res_webpay_data["TBK_MONTO"]
                TBK_CODIGO_AUTORIZACION = res_webpay_data["TBK_CODIGO_AUTORIZACION"]
                TBK_FINAL_NUMERO_TARJETA = res_webpay_data["TBK_FINAL_NUMERO_TARJETA"]
                TBK_HORA_TRANSACCION = str(res_webpay_data["TBK_HORA_TRANSACCION"])
                TBK_ID_TRANSACCION = res_webpay_data["TBK_ID_TRANSACCION"]
                TBK_TIPO_PAGO = res_webpay_data["TBK_TIPO_PAGO"]
                TBK_NUMERO_CUOTAS = res_webpay_data["TBK_NUMERO_CUOTAS"]
                TBK_FECHA_TRANSACCION = str(res_webpay_data["TBK_FECHA_TRANSACCION"])
                TBK_ID_SESION = str(res_webpay_data["TBK_ID_SESION"])


                anno_transaccion = TBK_ID_SESION[:4] 
                mes_transaccion = TBK_ID_SESION[4:6]
                dia_transaccion = TBK_ID_SESION[6:8]

                TBK_FECHA_TRANSACCION = "{year}-{mes}-{dia}".format(year=anno_transaccion,mes=mes_transaccion,dia=dia_transaccion)

                hora_transaccion = TBK_ID_SESION[8:10]
                minutos_transaccion = TBK_ID_SESION[10:12]
                segundo_transaccion = TBK_ID_SESION[12:14]

                TBK_HORA_TRANSACCION = "{hora}:{minutos}:{segundos}".format(hora=hora_transaccion,minutos=minutos_transaccion,segundos=segundo_transaccion)

                TBK_TIPO_CUOTA = TBK_TIPO_PAGO

                if TBK_TIPO_PAGO == "VD":
                    TBK_TIPO_PAGO = "Redcompra"
                else:
                    TBK_TIPO_PAGO = "Crédito"

                if TBK_TIPO_CUOTA == "VN":
                    TBK_TIPO_CUOTA = "Sin Cuotas"
                elif TBK_TIPO_CUOTA == "VC":
                    TBK_TIPO_CUOTA = "Cuotas Normales"
                elif TBK_TIPO_CUOTA == "SI":
                    TBK_TIPO_CUOTA = "Sin interés"
                elif TBK_TIPO_CUOTA == "CI":
                    TBK_TIPO_CUOTA = "Cuotas Comercio"
                elif TBK_TIPO_CUOTA == "VD":
                    TBK_TIPO_CUOTA = "Débito"

                webpay_data = {
                    "TBK_ORDEN_COMPRA":TBK_ORDEN_COMPRA,
                    "TBK_MONTO":int(TBK_MONTO),
                    "TBK_CODIGO_AUTORIZACION":TBK_CODIGO_AUTORIZACION,
                    "TBK_FINAL_NUMERO_TARJETA":TBK_FINAL_NUMERO_TARJETA,
                    "TBK_HORA_TRANSACCION":TBK_HORA_TRANSACCION,
                    "TBK_ID_TRANSACCION":TBK_ID_TRANSACCION,
                    "TBK_TIPO_PAGO":TBK_TIPO_PAGO,
                    "TBK_NUMERO_CUOTAS":TBK_NUMERO_CUOTAS,
                    "TBK_FECHA_TRANSACCION":TBK_FECHA_TRANSACCION,
                    "TBK_HORA_TRANSACCION":TBK_HORA_TRANSACCION,
                    "TBK_TIPO_CUOTA":TBK_TIPO_CUOTA,
                    "TBK_ID_SESION":TBK_ID_SESION
                }

            else:
                print res_webpay["error"]

        if order_id == "":
            self.render("order_detail/list.html",dn="Pedido solicitado no existe",order_detail=od_list,order=order, webpay_data=webpay_data)
        else:
            try:
                response = order_detail.ListByOrderId(order_id)
                if "success" in response:
                    od_list = response["success"]
                    self.render("order_detail/list.html",dn="",order_detail=od_list,order=order, webpay_data=webpay_data)
                else:
                    self.render("order_detail/list.html",dn=response["error"],order_detail=od_list,order=order, webpay_data=webpay_data)
            except Exception, e:
                self.render("order_detail/list.html",dn="bpf",error=str(e),order_detail=od_list,order=order, webpay_data=webpay_data)

            


class AddOrderDetailHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self):
        order_detail = OrderDetail()
        self.render("order_detail/save.html",dn="",mode="add", order_detail=order_detail)

    @tornado.web.authenticated
    def post(self):

        order_id = self.get_argument("order_id","")
        product_id = self.get_argument("product_id","")
        quantity = self.get_argument("quantity","")
        total = self.get_argument("total","")

        order_detail = OrderDetail()

        if order_id == "" or product_id == "" or quantity == "" or total == "":
            self.render("order_detail/save.html",dn="Error al insertar detalle de pedido", order_detail=order_detail, mode="add")

        
        order_detail.order_id = order_id
        order_detail.product_id = product_id
        order_detail.quantity = quantity
        order_detail.total = total
        order_detail.Save()

        self.render("order_detail/save.html",dn="Detalle insertado correctamente",order_detail=order_detail, mode="add")        

class EditOrderDetailHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self):
        self.render("order_detail/save.html",dn="",mode="edit",order_detail=order_detail)