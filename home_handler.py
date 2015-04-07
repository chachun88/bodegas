#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import xlrd  # lib excel
import os
import urllib

from basehandler import BaseHandler
from model.product import Product
from model.cellar import Cellar
from globals import Menu, dir_products, dir_stock, debugMode

fn = ''
fnout = ''


class HomeHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):

        self.set_active(Menu.PRODUCTOS_CARGA_STOCK)  # change menu active item

        dn = self.get_argument("dn", "f")
        w = []

        if self.get_argument("w", "") != "":
            w = self.get_argument("w", "").split( "," )

        self.render("product/home.html", side_menu=self.side_menu, dn=dn, w=w)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        # upload file 
        try:  # Windows needs stdio set for binary mode.
            import msvcrt
            msvcrt.setmode(0, os.O_BINARY)  # stdin  = 0
            msvcrt.setmode(1, os.O_BINARY)  # stdout = 1
        except ImportError:
            pass

        fileitem = ''
        # A nested FieldStorage instance holds the file
        try:
            fileitem = self.request.files['file'][0]
        except:
            pass

        # strip leading path from file name to avoid directory traversal attacks        

        if fileitem != "":

            fn = fileitem['filename']
            open(dir_stock + fn, 'wb').write(fileitem["body"])

            try:

                doc = xlrd.open_workbook(dir_stock + fn)

                sheet = doc.sheet_by_index(0)

                nrows = sheet.nrows
                ncols = sheet.ncols
                # print ncols
                # self.write("{}".format(ncols))

                matriz = []

                for i in range(nrows):
                    matriz.append([])
                    for j in range(ncols):
                        matriz[i].append(sheet.cell_value(i,j))

                args = {
                    "side_menu" : self.side_menu, 
                    "matriz" : matriz, 
                    "nrows" : nrows, 
                    "ncols" : ncols, 
                    "dn" : "t", 
                    "w" : "",
                    "filename" : fn
                }

                self.render("product/home.html", args=args)

            except ImportError:
                pass

        else:
            args = {
                "side_menu" : self.side_menu, 
                "ncols" : ncols, 
                "dn" : "t2", 
                "w" : "",
                "filename" : ""
            }
            self.render("product/home.html", args)


class ProductLoadHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self): 

        warnings = []

        fn = self.get_argument("filename", "")

        if debugMode:
            print fn

        if fn != "":

            doc = xlrd.open_workbook(dir_products + fn)

            sheet = doc.sheet_by_index(0)

            nrows = sheet.nrows
            ncols = sheet.ncols
            print ncols
            # self.write("{}".format(ncols))

            # fila
            for i in range(1, nrows):

                prod = Product()

                # columna
                for j in range(ncols):

                    if j == 0:
                        prod.category = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 1:
                        prod.sku = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 2:
                        prod.name = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 3:
                        prod.description = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 4:                                        
                        prod.color = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 5:                                        
                        prod.price = int(sheet.cell_value(i,j))
                    elif j == 6:
                        prod.sell_price = int(sheet.cell_value(i,j))
                    elif j == 7:

                        bulk_price = sheet.cell_value(i,j)

                        if bulk_price != "":
                            prod.bulk_price = int(bulk_price)

                    elif j == 8:
                        prod.manufacturer = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 9:
                        prod.brand = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 10:
                        valor = sheet.cell_value(i,j)

                        if type(valor) is unicode:
                            prod.size = valor.encode("utf-8")
                        else:
                            prod.size = str(valor)
                    elif j == 11:
                        prod.delivery = sheet.cell_value(i,j).encode("utf-8")
                    elif j == 12:
                        prod.which_size = sheet.cell_value(i,j).encode("utf-8")

                if debugMode:
                    print "product name : {}".format(prod.name)

                res_save = prod.Save("one")

                if debugMode:
                    if "error" in res_save:
                        print res_save["error"]

        if len(warnings) > 0:
            # self.render("/product/out?dn={dn}&w={warnings}".format(dn="t2",warnings=",".join(warnings)))
            args = {
                "dn" : "t2",
                "warnings" : ",".join(warnings),
                "filename" : ""
            }
            self.redirect("/product/out?" + urllib.urlencode(args))
        else:
            # self.render("/product/out?dn={dn}&w={warnings}".format(dn="t",warnings=",".join(warnings)))
            args = {
                "dn" : "t",
                "warnings" : ",".join(warnings),
                "filename" : ""
            }
            self.redirect("/product/out?" + urllib.urlencode(args))


class ProductRemoveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        prod = Product()
        prod.InitWithId(self.get_argument("id", ""))

        cellar_id = "remove"
        size = "remove"

        cellar = Cellar()       
        product_find = cellar.ProductKardex(prod.sku, cellar_id, size)

        buy = 0
        sell = 0

        for p in product_find:

            if p["operation_type"] == "buy":
                buy = p["total"]  

            if p["operation_type"] == "sell":
                sell = p["total"]

        units = buy-sell  

        if units > 0:
            self.render("product/list.html", dn="bpf", side_menu=self.side_menu, product_list=prod.get_product_list())  
        else:

            prod.Remove()   

            self.render("product/list.html", dn="bpt", side_menu=self.side_menu, product_list=prod.get_product_list())
            # self.redirect("/product/list")


class ProductOutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.PRODUCTOS_CARGA_MASIVA)  # change menu active item

        dn = self.get_argument("dn", "f")

        filename = self.get_argument("filename", "")

        args = {
            "side_menu" : self.side_menu, 
            "dn": dn,
            "filename" : filename
        }

        self.render("product/out.html", args=args)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        filename = self.get_argument("filename", "")

        # upload file 
        try:  # Windows needs stdio set for binary mode.
            import msvcrt
            msvcrt.setmode(0, os.O_BINARY)  # stdin  = 0
            msvcrt.setmode(1, os.O_BINARY)  # stdout = 1
        except ImportError:
            pass

        fileitem = ''

        try:
            # A nested FieldStorage instance holds the file
            fileitem = self.request.files['file'][0]
        except:
            pass

        # strip leading path from file name to avoid directory traversal attacks

        if fileitem != "":

            filename = fileitem['filename']

            # chegk if directory exists
            try:
                os.stat( dir_products )
            except:
                os.mkdir(dir_products)

            open(dir_products + filename, 'wb').write(fileitem["body"])
            # message = 'The file "' + fn + '" was uploaded successfully'

            try:

                doc = xlrd.open_workbook(dir_products + filename)

                sheet = doc.sheet_by_index(0)

                nrows = sheet.nrows
                ncols = sheet.ncols
                # print ncols
                # self.write("{}".format(ncols))

                matriz = []

                for i in range(nrows):
                    matriz.append([])
                    for j in range(ncols):
                        matriz[i].append(sheet.cell_value(i,j))

                args = {
                    "side_menu" : self.side_menu,
                    "dn" : "f",
                    "matriz" : matriz,
                    "nrows" : nrows,
                    "ncols" : ncols,
                    "filename" : filename
                }

                self.render("product/out.html", args=args)

            except ImportError:
                pass
        else:
            args = {
                "side_menu" : self.side_menu,
                "dn" : "t2",
                "matriz" : matriz,
                "nrows" : nrows,
                "ncols" : ncols,
                "filename" : filename
            }
            self.render("product/out.html", args)


class ProductMassiveOutputHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):

        fn = self.get_argument("filename", "")

        if fn != "":

            doc = xlrd.open_workbook(dir_stock + fn)

            sheet = doc.sheet_by_index(0)        

            for i in range(1, sheet.nrows): 

                for j in range(sheet.ncols):  

                    if j == 0:
                        sku = sheet.cell_value(i,j)
                    elif j == 1:
                        size = sheet.cell_value(i,j)
                    elif j == 2:
                        entrada = sheet.cell_value(i,j)
                    elif j == 3:
                        salida = sheet.cell_value(i,j)
