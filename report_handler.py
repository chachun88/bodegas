#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import csv


from bson import json_util
from basehandler import BaseHandler
from globals import Menu
from model10.cellar import Cellar
from model10.product import Product


class ReportHandler(BaseHandler):

    data = []

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.INFORMES_POR_BODEGA)

        day = self.get_argument("day", "today")
        fromm = self.get_argument("from", "from")
        until = self.get_argument("until", "until")

        data = Cellar().ListKardex(day, fromm, until)

        self.render("report/home.html", 
                    side_menu=self.side_menu, 
                    data=data,
                    data_str=json_util.dumps(data))

    @tornado.web.authenticated
    def post(self):

        self.set_active(Menu.INFORMES_POR_BODEGA)

        day = self.get_argument("day", "")
        fromm = self.get_argument("from", "")
        until = self.get_argument("until", "")

        data = Cellar().ListKardex(day, fromm, until)

        self.render("report/period.html", 
                    side_menu=self.side_menu, 
                    data=data, 
                    data_str=json_util.dumps(data))

    def check_xsrf_cookie(self):
        pass


class ReportUploadHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    def post(self):

        data_str = self.get_argument("load", "")

        data = json_util.loads(data_str)

        cellar = Cellar().List(1, 100)
        # data = json_util.dumps(len(data))

        tit = ["SKU", "Talla", "Precio U. Compra", "Precio U. Venta",
               "Cantidad", "Total", "Usuario", "Bodega"]

        item_length = len(data)

        matriz = []

        for i in range(item_length):
            matriz.append([])
            if "product_sku" in data[i]:
                matriz[i].append(data[i]["product_sku"])
            if "size" in data[i]:
                matriz[i].append(data[i]["size"])
            if "balance_price" in data[i]:
                matriz[i].append(data[i]["balance_price"])
            if "sell_price" in data[i]:
                matriz[i].append(data[i]["sell_price"])
            if "units" in data[i]:
                matriz[i].append(data[i]["units"])
            if "sell_price" in data[i] and "units" in data[i]:
                total = int(data[i]["sell_price"]) * int(data[i]["units"])
                matriz[i].append(total)
            if "user" in data[i]:
                matriz[i].append(data[i]["user"])

            for c in cellar:
                # print "DATA:{}".format(data[i])
                if data[i]["cellar_id"] == str(c["id"]):
                    matriz[i].append(c["name"])

        tras = zip(*matriz)

        # lol = [[1,2,3],[4,5,6],[7,8,9]]
        # print lol
        item_length = len(tras[0])

        with open('uploads/informe.csv', 'wb') as test_file:
            file_writer = csv.writer(test_file, delimiter=';')
            file_writer.writerow([x for x in tit])
            for i in range(item_length):
                file_writer.writerow([x[i] for x in tras])

    def check_xsrf_cookie(self):
        pass
