#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import os

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import glob

from bson import json_util

from basehandler import BaseHandler
from ..globals import *
from ..model10.product import Product
from ..model10.category import Category
from ..model10.tag import Tag
from ..model10.kardex import Kardex
from ..model10.size import Size
from ..model10.cellar import Cellar


class ProductAddHandler(BaseHandler):

    def saveImage( self, imagedata, sku, image_number ):

        final_name = "{}_{}.png".format( image_number, sku )

        try:

            file_path = dir_img + final_name

            self.deleteOtherImages( final_name )

            try:
                os.stat(dir_img)
            except:
                os.makedirs(dir_img)

            open(file_path, 'wb').write(imagedata["body"])

        except Exception, e:
            print str(e)
            pass

        return final_name

    def deleteOtherImages(self, image_name):

        # print "files {}".format( image_name )

        if image_name != "":
            if os.path.isdir(dir_img):
                os.chdir( dir_img )
                for file in glob.glob("*" + image_name):
                    try:
                        os.remove( file )
                    except Exception, e:
                        print "no se elimino : {}".format( str(e) )
                        pass

                os.chdir("../../")

                self.write("imagen eliminada")
            else:
                os.makedirs(dir_img)
                self.write("directorio de imagen acaba de ser")
        else:
            self.write( "imagen no existe " )

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.PRODUCTOS_CARGA)  # change menu active item

        pjax = bool(self.get_argument("_pjax", False))

        tags = []
        tag = Tag()
        res_tags = tag.List(1,100000)

        sizes = []
        size = Size()
        res_sizes = size.list()

        if "success" in res_sizes:
            sizes = res_sizes["success"]

        if "success" in res_tags:
            tags = res_tags["success"]

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        prod = Product()
        self.render("product{}/add.html".format(pjax_str), dn="", side_menu=self.side_menu, product=prod, tit="add", tags=tags, sizes=sizes)

    @tornado.web.authenticated
    def post(self):

        try:  # Windows needs stdio set for binary mode.
            import msvcrt
            msvcrt.setmode(0, os.O_BINARY)  # stdin  = 0
            msvcrt.setmode(1, os.O_BINARY)  # stdout = 1
        except ImportError:
            pass

        ''' 
        fn =""    
        try:   
            form = cgi.FieldStorage()

            # A nested FieldStorage instance holds the file
            fileitem = self.request.files['image'][0]

            for i in self.request.files:
                self.write("llega : {} <br>".format( self.request.files[i][0]["filename"] ))

            # strip leading path from file name to avoid directory traversal attacks
            fn = fileitem['filename']
        except:
            pass

        return
        '''

        '''
        if fn != "":
            #print fn 
            open('uploads/images/' + self.get_argument("sku", "")+'.png', 'wb').write(fileitem["body"])
            image_name=self.get_argument("sku", "")+'.png'
        else:
            image_name=''
        '''

        # if the category does not exist is created
        category = Category()

        try:
            category.InitWithName(self.get_argument("category", ""))
        except:
            category.name = self.get_argument("category", "")
            category.Save()  

        prod = Product()

        res = prod.InitBySku(self.get_argument("sku", ""))

        # print res

        # print "type:{} value:{}".format(type(res),res)

        image_order = self.get_argument("image_order", "").encode("utf-8").strip().split(",")
        filelist = self.request.files
        product_sku = self.get_argument("sku", "")

        photolist = ['','','','','','']

        new_list = ['','','','','','']

        if "success" in res:

            photolist[0] = prod.image
            photolist[1] = prod.image_2
            photolist[2] = prod.image_3
            photolist[3] = prod.image_4
            photolist[4] = prod.image_5
            photolist[5] = prod.image_6

            index = 0
            for order in image_order:
                if order != '':
                    if "image" in filelist:
                        filename = self.saveImage( filelist["image"][int(order)], product_sku, index )
                        new_list[index] = filename
                    else:
                        new_list[index] = photolist[int(order)]
                    index += 1

            # print new_list

            prod.category   = self.get_argument("category", "")
            prod.sku        = self.get_argument("sku", "")
            prod.name       = self.get_argument("name", "").encode('utf-8')
            prod.upc        = self.get_argument("upc", "")
            prod.description = self.get_argument("description", "")
            prod.brand      = self.get_argument("brand", "").encode('utf-8')
            prod.manufacturer = self.get_argument("manufacturer", "")
            prod.size        = self.get_arguments("size")
            prod.color      = self.get_argument("color", "")
            prod.material   = self.get_argument("material", "")
            prod.bullet_1   = self.get_argument("bullet_1", "")
            prod.bullet_2   = self.get_argument("bullet_2", "") 
            prod.bullet_3   = self.get_argument("bullet_3", "")
            prod.currency   = self.get_argument("currency", "")
            prod.price      = self.get_argument("price", "")
            prod.image      = new_list[0]
            prod.image_2    = new_list[1]
            prod.image_3    = new_list[2]
            prod.image_4    = new_list[3]
            prod.image_5    = new_list[4]
            prod.image_6    = new_list[5]
            prod.sell_price = self.get_argument("sell_price",0)
            prod.delivery   = self.get_argument("delivery","").encode('utf-8')
            prod.which_size = self.get_argument("which_size","").encode('utf-8')
            prod.tags       = ",".join([t.encode("utf-8") for t in self.get_arguments("tags")])
            prod.for_sale   = self.get_argument("for_sale",0)

            promotion_price = self.get_argument("promotion_price", 0)
            if promotion_price != "":
                prod.promotion_price = promotion_price
            prod.bulk_price = self.get_argument("bulk_price", 0)

            # print self.get_arguments("tags")

            res_save = prod.Save()

            # print res_save

            if "success" in res_save:
                self.render("message.html",msg="El producto ha sido guardado exitosamente")
            else:
                # self.redirect("/product/edit?id={}".format(prod.identifier))
                self.write(res_save["error"])

        else:

            for x in range(6):
                photolist[x] = "{}_{}.png".format(x, product_sku.encode('utf-8'))

            # print image_order
            index = 0
            for order in image_order:
                if order != '':
                    if "image" in filelist:
                        filename = self.saveImage( filelist["image"][int(order)], product_sku, index )
                        new_list[index] = filename
                    else:
                        new_list[index] = photolist[int(order)]
                    index += 1

            prod.category   = self.get_argument("category", "").encode("utf-8")
            prod.sku        = self.get_argument("sku", "").encode("utf-8")
            prod.name       = self.get_argument("name", "").encode("utf-8")
            prod.upc        = self.get_argument("upc", "").encode("utf-8")
            prod.description = self.get_argument("description", "")
            prod.brand      = self.get_argument("brand", "").encode("utf-8")
            prod.manufacturer = self.get_argument("manufacturer", "").encode("utf-8")
            prod.color      = self.get_argument("color", "")
            prod.material   = self.get_argument("material", "").encode("utf-8")
            prod.bullet_1   = self.get_argument("bullet_1", "").encode("utf-8")
            prod.bullet_2   = self.get_argument("bullet_2", "").encode("utf-8")
            prod.bullet_3   = self.get_argument("bullet_3", "").encode("utf-8")
            prod.currency   = self.get_argument("currency", "").encode("utf-8")
            prod.price      = self.get_argument("price", "").encode("utf-8")
            prod.image      = new_list[0].encode("utf-8")
            prod.image_2    = new_list[1].encode("utf-8")
            prod.image_3    = new_list[2].encode("utf-8")
            prod.image_4    = new_list[3].encode("utf-8")
            prod.image_5    = new_list[4].encode("utf-8")
            prod.image_6    = new_list[5].encode("utf-8")
            prod.sell_price = self.get_argument("sell_price",0).encode("utf-8")
            prod.delivery   = self.get_argument("delivery","").encode("utf-8")
            prod.which_size = self.get_argument("which_size","").encode("utf-8")
            prod.for_sale   = self.get_argument("for_sale",0)
            promotion_price = self.get_argument("promotion_price", 0)
            if promotion_price != "":
                prod.promotion_price = promotion_price
            prod.bulk_price = self.get_argument("bulk_price", 0)

            # size_arr = self.get_argument("size", "").split(",")
            # size_arr = [s.encode("utf-8") for s in size_arr]

            prod.size        = self.get_arguments("size")
            prod.tags       = ",".join([t.encode("utf-8") for t in self.get_arguments("tags","")])

            respose = prod.Save("one")

            # print respose

            if "success" in respose:
                self.redirect("/product/list")
            else:
                self.write(respose["error"])


class ProductEditHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.PRODUCTOS_CARGA)

        pjax = bool(self.get_argument("_pjax", False))

        prod = Product()
        res = prod.InitById(self.get_argument("id", ""))

        tags = []
        tag = Tag()
        res_tags = tag.List(1,100000)

        sizes = []
        size = Size()
        res_sizes = size.list()

        if "success" in res_sizes:
            sizes = res_sizes["success"]
        elif debugMode:
            print res_sizes["error"]

        if "success" in res_tags:
            tags = res_tags["success"]
        elif debugMode:
            print res_tags["error"]

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        if "success" in res:
            self.render("product{}/edit.html".format(pjax_str), dn="", side_menu=self.side_menu, product=prod, tit="edit", tags=tags, sizes=sizes)
        else:
            self.render("product{}/add.html".format(pjax_str), dn="bpf", side_menu=self.side_menu, product=prod, tit="edit", tags=tags, sizes=sizes)


class FastEditHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):

        prod = Product()

        res = prod.InitById(self.get_argument("id", ""))

        if "success" in res:

            prod.name = self.get_argument("name", "")
            prod.description = self.get_argument("description", "")
            prod.color = self.get_argument("color", "")
            prod.price = self.get_argument("price", "")
            prod.sell_price     = self.get_argument("sell_price", "")
            prod.category = self.get_argument("category","")
            prod.sku = prod.sku
            # prod.manufacturer = self.get_argument("manufacturer","")
            # prod.brand = self.get_argument("brand","")
            # prod.which_size = self.get_argument("which_size","")
            # prod.for_sale = self.get_argument("for_sale",0)
            prod.position = self.get_argument("position", 1)
            promotion_price = self.get_argument("promotion_price", 0)
            if promotion_price != "":
                prod.promotion_price = promotion_price
            prod.bulk_price = self.get_argument("bulk_price", 0)

            prod.tags = ','.join(str(v) for v in prod.tags)

            respuesta = prod.Save()

            self.write(respuesta)

        else:
            self.write(res)


class ForSaleHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        product_id = self.get_argument("product_id","")

        if product_id.isnumeric():
            prod = Product()
            self.write(json_util.dumps(prod.ForSale(product_id)))
        else:
            self.write(json_util.dumps({"error":"Product ID proporcionado es inválido"}))


class CheckStockHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        product_sku = self.get_argument("product_sku", "")
        size_name = self.get_argument("size_name", "")

        if product_sku != "":

            if size_name != "":

                size = Size()
                size.name = size_name

                res_size_name = size.initByName()

                if "success" in res_size_name:

                    kardex = Kardex()
                    res_stock = kardex.stockByProductSku(product_sku, size.id)

                    self.write(json_util.dumps(res_stock))

                else:

                    self.write(json_util.dumps(res_size_name))

            else:
                self.write(json_util.dumps(self.showError("size_id esta vacio")))

        else:
            self.write(json_util.dumps(self.showError("product_sku esta vacio")))


class ProductRemoveHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        prod = Product()
        prod.InitById(self.get_argument("id", ""))

        cellar_id = "remove"
        size = "remove"

        cellar = Cellar()       
        product_find = cellar.FindProductKardex(prod.sku, cellar_id, size)

        units = 0

        if "success" in product_find:
            units = product_find["success"]

        product_list = []

        res_product_list = prod.GetList()

        if "success" in res_product_list:
            product_list = res_product_list["success"]

        if units > 0:
            # self.render("product/list.html", dn="bpf", side_menu=self.side_menu, product_list=product_list)
            self.redirect("/product/list?dn=bpf")
        else:

            res_remove = prod.Remove()

            if "success" in res_remove:
                self.redirect("/product/list")
            else:
                self.redirect("/product/list?dn=bpe&message={}".format(res_remove["error"]))
                # self.render("product/list.html", dn="bpe", side_menu=self.side_menu, product_list=product_list, message=res_remove["error"])


class ChangePositionHandler(BaseHandler):

    def post(self):
        product_id = self.get_argument("product_id", "")
        position = self.get_argument("position", "")

        if product_id == '' or position == '':
            self.write("product id or position is null")
        else:
            product = Product()
            response = product.changePosition(product_id, position)
            self.write(response)
