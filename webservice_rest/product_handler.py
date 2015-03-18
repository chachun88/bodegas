#!/usr/bin/python
# -*- coding: UTF-8 -*-

from model10.product import Product

from base_handler import BaseHandler
from model10.kardex import Kardex
from bson import json_util


class AddProductHandler(BaseHandler):

    def post(self):

        # validate access token
        if not self.ValidateToken():
            return

        # isntantitate product
        product = Product()

        product.category = self.get_argument("category", "")
        product.sku = self.get_argument("sku", "")
        product.name = self.get_argument("name", "")
        product.upc = self.get_argument("upc", "")
        product.description = self.get_argument("description", "")
        product.brand = self.get_argument("brand", "")
        product.manufacturer = self.get_argument("manufacturer", "")
        product.size = self.get_argument("size", "")
        product.color = self.get_argument("color", "")
        product.material = self.get_argument("material", "")
        product.bullet_point_1 = self.get_argument("bullet_1", "")
        product.bullet_point_2 = self.get_argument("bullet_2", "")
        product.bullet_point_3 = self.get_argument("bullet_3", "")
        product.price = self.get_argument("price", "")
        product.promotion_price = self.get_argument("promotion_price", 0)
        product.image = self.get_argument("image", "")
        product.image_2 = self.get_argument("image_2", "")
        product.image_3 = self.get_argument("image_3", "")
        product.image_4 = self.get_argument("image_4", "")
        product.image_5 = self.get_argument("image_5", "")
        product.image_6 = self.get_argument("image_6", "")
        product.sell_price = self.get_argument("sell_price", 0)
        product.tags = self.get_argument("tags", "")  # se obtiene como string
        product.delivery = self.get_argument("delivery", "")
        product.which_size = self.get_argument("which_size", "")
        product.id = self.get_argument("id", "")
        product.size_id = self.get_argument("size_id", "")

        # self.write(product.sku)
        # return

        # saving current product
        oid = json_util.dumps(product.Save())

        self.write(oid)


class RemoveProductHandler(BaseHandler):

    def get(self):
        # validate access token
        if not self.ValidateToken():
            return

        idd = self.get_argument("id", "")
        sku = self.get_argument("sku", "")

        product = Product()

        if idd != "":
            product.id = idd
        else:
            product.sku = sku

        self.write(json_util.dumps(product.Remove()))


class GetProductHandler(BaseHandler):

    def get(self):

        # validate access token
        if not self.ValidateToken():
            return

        idd = self.get_argument("id", "")
        sku = self.get_argument("sku", "")

        product = Product()

        if idd != "":
            self.write(json_util.dumps(product.InitById(idd)))
            # json_util.dumps(product.Print()))
        else:
            self.write(json_util.dumps(product.InitBySku(sku)))
            # self.write(json_util.dumps(product.Print()))


class ListProductsHandler(BaseHandler):

    def get(self):

        # validate access token
        if not self.ValidateToken():
            return

        current_page = "1"
        items_per_page = "10"
        product = Product()

        try:
            current_page = int(self.get_argument("page", "1"))
            items_per_page = int(self.get_argument("items", "10"))
        except Exception, e:
            print str(e)

        self.write(
            json_util.dumps(product.GetList(current_page, items_per_page)))


class UploadPictureSampleHandler(BaseHandler):

    def get(self):
        self.render("test_upload.html")


class UploadPictureHandler(BaseHandler):

    def get(self):
        pass

    def post(self):

        # validate
        if not self.ValidateToken():
            return

        try:
            image = self.request.files['image'][0]

            output_file = open("uploads/" + image['filename'], 'w')
            output_file.write(image['body'])

            image_number = self.get_argument("number")
            product_id = self.get_argument("id")

            self.finish('se ha subido la imagen')
        except Exception, e:
            self.write(str(e))
            self.finish('se ha producido un error al subir la imagen')


class SearchHandler(BaseHandler):

    def get(self):
        query = self.get_argument("q", "")

        product = Product()
        self.write(json_util.dumps(product.Search(query)))


class ForSaleHandler(BaseHandler):

    def post(self):

        product_id = self.get_argument("product_id", "")

        if product_id.isnumeric():
            prod = Product()
            self.write(json_util.dumps(prod.ForSale(product_id)))
        else:
            self.write(
                json_util.dumps({"error": "Product ID proporcionado es inválido"}))


class CheckStockHandler(BaseHandler):

    def post(self):

        product_id = self.get_argument("product_id", "")
        size_id = self.get_argument("size_id", "")

        if product_id != "":
            if size_id != "":
                kardex = Kardex()
                res_stock = kardex.stockByProductId(product_id, size_id)
                self.write(json_util.dumps(res_stock))
            else:
                self.write(json_util.dumps({"error": "size id esta vacio"}))
        else:
            self.write(json_util.dumps({"error": "product id esta vacio"}))
