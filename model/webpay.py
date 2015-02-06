#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model.base_model import BaseModel
from bson import json_util
import urllib

class Webpay(BaseModel):

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def monto(self):
        return self._monto
    @monto.setter
    def monto(self, value):
        self._monto = value
    
    @property
    def codigo_autorizacion(self):
        return self._codigo_autorizacion
    @codigo_autorizacion.setter
    def codigo_autorizacion(self, value):
        self._codigo_autorizacion = value

    @property
    def final_numero_tarjeta(self):
        return self._final_numero_tarjeta
    @final_numero_tarjeta.setter
    def final_numero_tarjeta(self, value):
        self._final_numero_tarjeta = value

    @property
    def fecha_contable(self):
        return self._fecha_contable
    @fecha_contable.setter
    def fecha_contable(self, value):
        self._fecha_contable = value
    
    @property
    def fecha_transaccion(self):
        return self._fecha_transaccion
    @fecha_transaccion.setter
    def fecha_transaccion(self, value):
        self._fecha_transaccion = value
    
    @property
    def hora_transaccion(self):
        return self._hora_transaccion
    @hora_transaccion.setter
    def hora_transaccion(self, value):
        self._hora_transaccion = value

    @property
    def id_transaccion(self):
        return self._id_transaccion
    @id_transaccion.setter
    def id_transaccion(self, value):
        self._id_transaccion = value
    
    @property
    def tipo_pago(self):
        return self._tipo_pago
    @tipo_pago.setter
    def tipo_pago(self, value):
        self._tipo_pago = value

    @property
    def numero_cuotas(self):
        return self._numero_cuotas
    @numero_cuotas.setter
    def numero_cuotas(self, value):
        self._numero_cuotas = value
            
    @property
    def id_sesion(self):
        return self._id_sesion
    @id_sesion.setter
    def id_sesion(self, value):
        self._id_sesion = value
    
    @property
    def orden_compra(self):
        return self._orden_compra
    @orden_compra.setter
    def orden_compra(self, value):
        self._orden_compra = value

    @property
    def order_id(self):
        return self._order_id
    @order_id.setter
    def order_id(self, value):
        self._order_id = value
    
    def __init__(self):
        BaseModel.__init__(self)
        self._id = ""
        self._monto = 0
        self._codigo_autorizacion = ""
        self._final_numero_tarjeta = ""
        self._fecha_contable = ""
        self._fecha_transaccion = ""
        self._hora_transaccion = ""
        self._id_transaccion = ""
        self._tipo_pago = ""
        self._numero_cuotas = 0
        self._id_sesion = ""
        self._orden_compra = ""
        self._order_id = ""

    def InitByOrderId(self, order_id):

        url = self.wsurl() + "/webpay/initbyorderid"

        data = {
        "token":self.token,
        "order_id":order_id
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        response_obj = json_util.loads(response_str)

        return response_obj


    
    