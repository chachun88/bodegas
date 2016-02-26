#!/usr/bin/python
# -*- coding: UTF-8 -*-


import dafiti
from product import Product
from basemodel import BaseModel


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

    def AddProduct(self, sku):
        p = Product()
        p.InitBySku(sku)

        # @todo:validate product here

        response = self.client.product.Create(
            sku, Name=p.name, Description=p.description, 
            Brand="Giani Da Firenze", Price=p.sell_price,
            PrimaryCategory=4, Variation="35")

        if response.type == dafiti.Response.ERROR:
            return

        # preparing images for dafiti
        images = [p.image, p.image_2, p.image_3, p.image_4, p.image_5, p.image_6]
        final_images = []

        for img in images:
            if img != '':
                final_images.append("http://bodegas.gianidafirenze.cl/image/{}?mw=1160".format(img))

        # adding images to dafiti
        response = self.client.product.Image(
            sku,
            *final_images)
