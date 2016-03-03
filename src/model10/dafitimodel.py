#!/usr/bin/python
# -*- coding: UTF-8 -*-


import dafiti
from product import Product
from size import Size
from kardex import Kardex
from cellar import Cellar
from basemodel import BaseModel
from datetime import date


class DafitiModel(BaseModel):

    def __init__(self):
        super(DafitiModel, self).__init__()

        self.client = dafiti.API(
                user_id='ricardo@loadingplay.com', 
                api_key='48f674c4a13c6af90063d8f70e3b23291f4ead79',
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
        s = Size()
        is_first = True

        image_skus = []

        create_requests = []
        update_requests = []

        for si in p.size_id:
            s.id = si
            s.initById()
            size = s.name

            if is_first:
                is_first = False
                new_sku = sku
            else:
                new_sku += "-{}".format(size)

            image_skus.append(new_sku)

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
            stock = self.getStock(sku, s.id)

            if not self.ProductExist(new_sku):

                create_requests.append(
                    dafiti.ProductRequest(
                        SellerSku=new_sku, Name=p.name, Description=p.description, 
                        Brand="Giani Da Firenze", Price=p.sell_price,
                        PrimaryCategory=main_category, Categories=categories.split(","),
                        Variation=size, ProductData=product_data,
                        Quantity=stock, ParentSku=sku))

            else:

                update_requests.append(
                    dafiti.ProductRequest(
                        SellerSku=new_sku, Name=p.name, Description=p.description, 
                        Brand="Giani Da Firenze", Price=p.sell_price,
                        PrimaryCategory=main_category, Categories=categories.split(","),
                        Variation=size, ProductData=product_data,
                        Quantity=stock, ParentSku=sku))

        self.client.product.sendPOST(dafiti.EndPoint.ProductCreate, create_requests)
        self.client.product.sendPOST(dafiti.EndPoint.ProductUpdate, update_requests)

        # preparing images for dafiti
        images = [p.image, p.image_2, p.image_3, p.image_4, p.image_5, p.image_6]
        final_images = []

        for img in images:
            if img != '':
                final_images.append("http://bgiani.ondev.today/image/dafiti/{}?mwh=1380,1160".format(img))

        # adding images to dafiti
        response = self.client.product.Image(
            image_skus,
            *final_images)

        print response.head

    def getStock(self, sku, size_id):

        c = Cellar()
        cellar = c.GetWebCellar()

        try:
            quantity = Kardex().FindKardex(sku, cellar['success'], size_id)["success"]["balance_units"]

            return quantity
        except:
            # there is no kardex
            return 0

    def GetCategories(self):
        r = self.client.category.Get()
        return r.body
