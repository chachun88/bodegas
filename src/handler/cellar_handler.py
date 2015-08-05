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


class CellarHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.BODEGAS_LISTAR)  # change menu active item

        pjax = bool(self.get_argument("_pjax", False))

        data = Cellar().List(1, 100)

        cellar = Cellar()

        web_cellar_id = None
        reservation_cellar_id = None

        res_web_cellar = cellar.GetWebCellar()
        res_reservation_cellar = cellar.GetReservationCellar()

        if "success" in res_web_cellar:
            web_cellar_id = res_web_cellar["success"]
        elif debugMode:
            print res_web_cellar["error"]

        if "success" in res_reservation_cellar:
            reservation_cellar_id = res_reservation_cellar["success"]
        elif debugMode:
            print res_web_cellar["error"]

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        self.render(
            "cellar{}/home.html".format(pjax_str),
            side_menu=self.side_menu, 
            data=data, 
            dn=self.get_argument("dn", ""), 
            web_cellar_id=web_cellar_id,
            reservation_cellar_id=reservation_cellar_id)


class CellarOutputHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

        cellar = Cellar()
        cellar.InitById(self.get_argument("id", ""))

        data = Cellar().List(1, 10)

        product = Product()
        # product.InitById(product_id)

        self.render("cellar/output.html", 
            operation="Salidas", 
            opp="out", 
            side_menu=self.side_menu, 
            cellar=cellar, 
            data=data, 
            product=product)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument("name", "")
        price = self.get_argument("price", "0")
        size = self.get_argument("size", "")
        color = self.get_argument("color", "")
        units = self.get_argument("units", "0")
        product_id = self.get_argument("product_id", "")
        cellar_id = self.get_argument("cellar_id", "")
        operation="sell"



        cellar = Cellar()
        cellar.InitById(cellar_id)

        product = Product()
        product.InitById(product_id)
        product_sku=product.sku

        redirect = "t"

        if "success" in cellar.RemoveProducts(product_sku, units, size, color, operation, self.get_user_email()):
            self.write("ok")
            redirect = "bpt"
        else:
            self.write("no")
            redirect = "bpf"

        self.redirect("/cellar?dn=" + redirect)

    def check_xsrf_cookie(self):
        pass


class CellarEasyInputHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

        cellar = Cellar()
        cellar.InitById(self.get_argument("id", ""))

        product = Product()
        res_lista = product.GetList()
        lista = []

        if "success" in res_lista:
            lista = res_lista["success"]

        size = Size()
        res_tallas = size.list()
        tallas = []

        if "success" in res_tallas:
            tallas = res_tallas["success"]

        products = []

        res_cellar_products = cellar.ListProducts()

        if "success" in res_cellar_products:
            products = res_cellar_products['success']

        self.render("cellar/easyinput.html", 
                    operation="Entradas ", 
                    opp="in", 
                    side_menu=self.side_menu, 
                    cellar=cellar, 
                    products=products, 
                    product_list=lista, 
                    tallas=tallas)

    @tornado.web.authenticated
    def post(self):

        cellar_id = self.get_argument("cellar_id", "")
        sku = self.get_argument("product_sku", "")
        quantity = self.get_argument("quantity", "")
        price = self.get_argument("price", 0)
        size = self.get_argument("size", "")
        operation = self.get_argument("operation", "buy")
        new_cellar = self.get_argument("new_cellar", "")

        _size = Size()
        _size.name = size
        res_size_name = _size.initByName()

        if "error" in res_size_name:
            self.write("no")
        else:
            cellar = Cellar()
            cellar.InitById(cellar_id)

            product = Product()
            init_sku = product.InitBySku(sku)

            if "success" in init_sku:

                kardex = Kardex()
                res_product_find = kardex.FindKardex(sku, cellar_id, _size.id)

                units = 0
                balance_price = 0

                # print res_product_find

                if "success" in res_product_find:

                    product_find = res_product_find["success"]
                    units = product_find["balance_units"]
                    balance_price = product_find["balance_price"]

                if operation == "buy":

                    kardex.product_sku = sku
                    kardex.units = quantity
                    kardex.price = price
                    kardex.size_id = _size.id
                    kardex.color = product.color
                    kardex.operation_type = Kardex.OPERATION_BUY
                    kardex.user = self.get_user_email()
                    kardex.cellar_identifier = cellar_id

                    res_add_product = kardex.Insert()

                    if "success" in res_add_product:
                        self.write("ok")
                    else:
                        self.write("no")
            else:
                self.write("no")

    ## invalidate xsfr cookie for ajax use
    def check_xsrf_cookie(self):
        pass

######################
#### easy output #####
######################
class CellarEasyOutputHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

        cellar = Cellar()
        cellar.InitById(self.get_argument("id", ""))

        data = Cellar().List(1, 100)

        size = Size()
        res_tallas = size.list()
        tallas = []

        if "success" in res_tallas:
            tallas = res_tallas["success"]

        c = Cellar()
        res_reservation = c.GetReservationCellar()

        reservation_cellar_id = None

        if "success" in res_reservation:
            reservation_cellar_id = res_reservation["success"]

        products = []

        res_cellar_products = cellar.ListProducts()

        if "success" in res_cellar_products:
            products = res_cellar_products['success']

        self.render("cellar/easyoutput.html", 
            cellar=cellar, 
            products=products, 
            cellarList=data,
            tallas=tallas,
            reservation_cellar_id=reservation_cellar_id)

    @tornado.web.authenticated
    def post(self):

        cellar_id = self.get_argument("cellar_id", "")
        sku = self.get_argument("product_sku", "")
        quantity = self.get_argument("quantity", "")
        price = self.get_argument("price", 0)
        size = self.get_argument("size", "")
        operation = self.get_argument("operation", "sell")
        new_cellar = self.get_argument("new_cellar", "")

        _size = Size()
        _size.name = size
        res_size_name = _size.initByName()

        if "error" in res_size_name:
            self.write("no")
        else:
            cellar = Cellar()
            cellar.InitById(cellar_id)

            product = Product()
            init_sku = product.InitBySku(sku)

            if "success" in init_sku:

                kardex = Kardex()
                res_product_find = kardex.FindKardex(sku, cellar_id, _size.id)

                units = 0
                balance_price = 0

                # print res_product_find

                if "success" in res_product_find:

                    product_find = res_product_find["success"]
                    units = product_find["balance_units"]
                    balance_price = product_find["balance_price"]

                if int(units) >= int(quantity): 

                    if operation == "mov":

                        kardex = Kardex()

                        kardex.product_sku = sku
                        kardex.units = quantity
                        kardex.price = balance_price
                        kardex.size_id = _size.id
                        kardex.color = product.color
                        kardex.operation_type = Kardex.OPERATION_MOV_OUT
                        kardex.user = self.get_user_email()
                        kardex.cellar_identifier = cellar_id

                        res_remove = kardex.Insert()

                        if "success" in res_remove:

                            kardex = Kardex()

                            kardex.product_sku = sku
                            kardex.units = quantity
                            kardex.price = balance_price
                            kardex.size_id = _size.id
                            kardex.color = product.color
                            kardex.operation_type = Kardex.OPERATION_MOV_IN
                            kardex.user = self.get_user_email()
                            kardex.cellar_identifier = new_cellar

                            res_add_product = kardex.Insert()

                            if "success" in res_add_product:
                                self.write("ok")
                            else:
                                self.write("no")
                        else:
                            self.write("no")                        

                    else:

                        kardex.product_sku = sku
                        kardex.units = quantity
                        kardex.sell_price = price
                        kardex.size_id = _size.id
                        kardex.color = product.color
                        kardex.operation_type = Kardex.OPERATION_SELL
                        kardex.user = self.get_user_email()

                        res_remove = kardex.Insert()

                        if "success" in res_remove:
                            self.write("ok")
                        else:
                            self.write("no")

                else:
                    self.write("no")
            else:
                self.write("no")


    ## invalidate xsfr cookie for ajax use
    def check_xsrf_cookie(self):
        pass



######################
#### cellar input ####
######################
class CellarInputHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.BODEGAS_LISTAR) #change menu active item

        cellar = Cellar()
        cellar.InitById(self.get_argument("id", ""))

        self.render("cellar/input.html",operation="Entradas ", opp="in", cellar=cellar)

    @tornado.web.authenticated
    def post(self):
        name = self.get_argument("name", "")
        price = self.get_argument("price", "0")
        units = self.get_argument("units", "0")
        product_id = self.get_argument("product_id", "")
        cellar_id = self.get_argument("cellar_id", "")
        size = self.get_argument("size", "")
        color = self.get_argument("color", "")
        operation= "buy"

        cellar = Cellar()
        response = cellar.InitById(cellar_id)

        if "success" in response:

            product = Product()
            response = product.InitById(product_id)

            if response == "ok":

                product_sku=product.sku

                product.size=size.split(",")
                product.color=color
                product.Save()

                redirect = "t"

                if "success" in cellar.AddProducts(product_sku, units, price, size, color, operation, self.get_user_email()):
                    self.write("ok")
                    redirect = "bpt"
                else:
                    self.write("no")
                    redirect = "bpf"

                self.redirect("/cellar?dn=" + redirect)

            else:
                self.write(response)

        else:
            self.write(response["error"])


class CellarDetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        idd = self.get_argument("id", "")

        pjax = bool(self.get_argument("_pjax", False))

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        cellar = Cellar()
        cellar.InitById(idd)
        # res = cellar.ListProducts()
        # productos = []

        # if "success" in res:
        #     productos = res["success"]
        # else:
        #     print res

        self.render("cellar{}/detail.html".format(pjax_str), side_menu=self.side_menu, cellar=cellar)

    @tornado.web.authenticated
    def post(self):

        idd = self.get_argument("id", "")
        start = int(self.get_argument("start", 0))
        items = int(self.get_argument("length", 20))
        term = self.get_argument("search[value]","")

        columns = [
            "sku",
            "name",
            "size",
            "color",
            "balance_units",
            "balance_total"
        ]

        column = int(self.get_argument("order[0][column]"))
        direction = self.get_argument("order[0][dir]")

        page = int(start / items) + 1

        cellar = Cellar()
        cellar.InitById(idd)
        res = cellar.ListProducts(page, items, columns[column], direction, term)
        productos = res["success"]

        if "success" in res:
            result = {
                "recordsTotal": cellar.TotalProducts(),
                "recordsFiltered": cellar.TotalProducts(term),
                "data": productos
            }
        else:
            print res

        self.write(json_util.dumps(result))

class CellarComboboxHandler(BaseHandler):   

    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    def post(self):
        
        product_id = self.get_argument("product_id", "")
        cellar_id = self.get_argument("cellar_id", "")

        cellar = Cellar()
        cellar.InitById(cellar_id)

        data = Cellar().List(1, 10)

        product = Product()
        product.InitById(product_id)

        self.render("cellar/combobox.html", operation="Salidas", opp="out", cellar=cellar, data=data, product=product)

    ## invalidate xsfr cookie for ajax use
    def check_xsrf_cookie(self):
        pass    

class SelectForSaleHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.BODEGAS_FORSALE)

        pjax = bool(self.get_argument("_pjax", False))

        cellar = Cellar()
        selected = cellar.GetWebCellar()
        data = Cellar().List(1, 100)

        cellar_id = ""

        if "success" in selected:
            cellar_id = selected["success"]

        pjax_str  = ''

        if pjax:
            pjax_str = '/ajax'

        self.render("cellar{}/selectforsale.html".format(pjax_str),cellars=data,cellar_id=cellar_id)

    @tornado.web.authenticated
    def post(self):

        cellar_id = self.get_argument("cellar_id","")

        if cellar_id != "":
            cellar = Cellar()
            self.write(json_util.dumps(cellar.SelectForSale(cellar_id)))
        else:
            self.write(json_util.dumps({"error":"Cellar id is not valid"}))


class SelectReservationHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.BODEGAS_RESERVATION)

        cellar = Cellar()
        selected = cellar.GetReservationCellar()
        data = Cellar().List(1, 100)

        pjax = bool(self.get_argument("_pjax", False))

        cellar_id = ""

        if "success" in selected:
            cellar_id = selected["success"]

        pjax_str  = ''

        if pjax:
            pjax_str = '/ajax'

        self.render("cellar{}/selectreservation.html".format(pjax_str),cellars=data,cellar_id=cellar_id)

    @tornado.web.authenticated
    def post(self):

        cellar_id = self.get_argument("cellar_id","")

        if cellar_id != "":
            cellar = Cellar()
            self.write(json_util.dumps(cellar.SelectReservation(cellar_id)))
        else:
            self.write(json_util.dumps({"error":"Cellar id is not valid"}))


class CellarEasyHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.BODEGAS_FACIL)

        pjax = bool(self.get_argument("_pjax", False))

        cellar = Cellar()
        res_list = cellar.FindById(self.current_user["cellar_permissions"])

        cellar_list = []

        if "success" in res_list:
            cellar_list = res_list["success"]

        product = Product()
        res_lista = product.GetList(0,0)
        lista = []

        if "success" in res_lista:
            lista = res_lista["success"]

        size = Size()
        res_tallas = size.list()
        tallas = []

        if "success" in res_tallas:
            tallas = res_tallas["success"]

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        self.render("cellar{}/easy.html".format(pjax_str), 
                    operation="Entradas ", 
                    opp="in", 
                    side_menu=self.side_menu, 
                    cellar_list=cellar_list, 
                    product_list=json_util.dumps(lista), 
                    products=lista,
                    tallas=tallas)

    @tornado.web.authenticated
    def post(self):

        cellar_id = self.get_argument("cellar_id", "")
        sku = self.get_argument("sku", "")
        quantity = self.get_argument("quantity", "")
        price = self.get_argument("price", 0)
        size = self.get_argument("size", "")
        operation = self.get_argument("operation", "")
        new_cellar = self.get_argument("new_cellar", "")

        _size = Size()
        _size.name = size
        res_size_name = _size.initByName()

        if "error" in res_size_name:
            self.write(json_util.dumps({"state": "error", "message": res_size_name["error"]}))
        else:
            cellar = Cellar()
            cellar.InitById(cellar_id)

            product = Product()
            init_sku = product.InitBySku(sku)

            if "success" in init_sku:

                kardex = Kardex()
                res_product_find = kardex.FindKardex(sku, cellar_id, _size.id)

                units = 0
                balance_price = 0

                # print res_product_find

                if "success" in res_product_find:

                    product_find = res_product_find["success"]
                    units = product_find["balance_units"]
                    balance_price = product_find["balance_price"]

                if operation == "buy":

                    kardex.product_sku = sku
                    kardex.units = quantity
                    kardex.price = price
                    kardex.size_id = _size.id
                    kardex.color = product.color
                    kardex.operation_type = Kardex.OPERATION_BUY
                    kardex.user = self.get_user_email()
                    kardex.cellar_identifier = cellar_id

                    res_add_product = kardex.Insert()

                    if "success" in res_add_product:
                        self.write(json_util.dumps({"state": "ok", "message": "Stock agregado exitosamente"}))
                    else:
                        self.write(json_util.dumps({"state": "error", "message": res_add_product["error"]}))
                else:

                    if int(units) >= int(quantity):

                        product = Product()
                        reserved = product.reserved(sku, size)

                        salidas_permitidas = int(units) - reserved

                        if int(quantity) > salidas_permitidas:
                            self.write(json_util.dumps({"state": "error", "message": "ERROR!!! cantidad supera {} unidade(s) permitidas(s)".format(salidas_permitidas)}))
                        else:
                            if operation == "mov":

                                kardex = Kardex()

                                kardex.product_sku = sku
                                kardex.units = quantity
                                kardex.price = balance_price
                                kardex.size_id = _size.id
                                kardex.color = product.color
                                kardex.operation_type = Kardex.OPERATION_MOV_OUT
                                kardex.user = self.get_user_email()
                                kardex.cellar_identifier = cellar_id

                                res_remove = kardex.Insert()

                                if "success" in res_remove:

                                    kardex = Kardex()

                                    kardex.product_sku = sku
                                    kardex.units = quantity
                                    kardex.price = balance_price
                                    kardex.size_id = _size.id
                                    kardex.color = product.color
                                    kardex.operation_type = Kardex.OPERATION_MOV_IN
                                    kardex.user = self.get_user_email()
                                    kardex.cellar_identifier = new_cellar

                                    res_add_product = kardex.Insert()

                                    if "success" in res_add_product:
                                        self.write(json_util.dumps({"state": "ok", "message": "Stock movido exitosamente"}))
                                    else:
                                        self.write(json_util.dumps({"state": "error", "message": res_add_product["error"]}))
                                else:
                                    self.write(json_util.dumps({"state": "error", "message": res_remove["error"]}))                        

                            else:

                                kardex.product_sku = sku
                                kardex.units = quantity
                                kardex.sell_price = price
                                kardex.size_id = _size.id
                                kardex.color = product.color
                                kardex.operation_type = Kardex.OPERATION_SELL
                                kardex.user = self.get_user_email()

                                res_remove = kardex.Insert()

                                if "success" in res_remove:
                                    self.write(json_util.dumps({"state": "ok", "message": "Stock sacado exitosamente"}))
                                else:
                                    self.write(json_util.dumps({"state": "error", "message": res_remove["error"]}))

                    else:
                        self.write(json_util.dumps({"state": "error", "message": "Stock insuficiente"}))
            else:
                self.write(json_util.dumps({"state": "error", "message": init_sku["error"]}))


    ## invalidate xsfr cookie for ajax use
    def check_xsrf_cookie(self):
        pass


class TestingHandler(BaseHandler):

    def get(self):
        order = Order()
        reserved = order.getReservedProducts()
        self.write(json_util.dumps(reserved))
