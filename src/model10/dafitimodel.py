#!/usr/bin/python
# -*- coding: UTF-8 -*-


import dafiti
from product import Product
from size import Size
from basemodel import BaseModel
from datetime import date


class DafitiModel(BaseModel):

    def __init__(self):
        super(DafitiModel, self).__init__()

        self.client = dafiti.API(
                user_id='julian@loadingplay.com', 
                api_key='1ce5e6b52a8665b677f7a8530ced6ae2ee82f89c',
                response_format='json')

    def ProductExist(self, sku):
        response = self.client.product.Get(
            SkuSellerList=[sku], 
            Filter=dafiti.Filter.All)

        if len(response.body["Products"]) > 0:
            return True
        else:
            return False

    def RemoveProduct(self, sku):
        self.client.product.Remove(sku)

    def AddProduct(self, sku, main_category, categories, color, season):
        p = Product()
        p.InitBySku(sku)

        sizes = []
        s = Size()

        for si in p.size_id:
            s.id = si
            s.initById()

            sizes.append(s.name)

        # @todo: resolver las tallas
        # for s in sizes:

        # @todo:validate product here
        product_data = {
            "Gender" : "Femenino",
            "ColorNameBrand" : p.color,
            "Color" : p.color,
            "ColorFamily" : color,
            "Season" : season,
            "SeasonYear" : date.today().year - 1
        }

        response = dafiti.Response()

        if not self.ProductExist(sku):

            response = self.client.product.Create(
                sku, Name=p.name, Description=p.description, 
                Brand="Giani Da Firenze", Price=p.sell_price,
                PrimaryCategory=main_category, Categories=categories.split(","),
                Variation=sizes[0], ProductData=product_data,
                Quantity=1)

            if response.type == dafiti.Response.ERROR:
                return

        else:
            response = self.client.product.Update(
                sku, Name=p.name, Description=p.description, 
                Brand="Giani Da Firenze", Price=p.sell_price,
                PrimaryCategory=main_category, Categories=categories.split(","),
                Variation=sizes[0], ProductData=product_data)

        # preparing images for dafiti
        images = [p.image, p.image_2, p.image_3, p.image_4, p.image_5, p.image_6]
        final_images = []

        for img in images:
            if img != '':
                final_images.append("http://bodegas.gianidafirenze.cl/image/{}?mw=1280".format(img))

        # adding images to dafiti
        response = self.client.product.Image(
            sku,
            *final_images)

    def GetCategories(self):
        r = self.client.category.Get()
        return r.body
