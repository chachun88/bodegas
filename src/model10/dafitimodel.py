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
            user_id='contacto@gianidafirenze.cl',
            api_key='aa8051656b6b1efab5b52615e2e4e2fe913b13d7',
            response_format='json',
            environment=dafiti.Environment.Live
        )

        # self.client = dafiti.API(
        #     user_id='julian@loadingplay.com',
        #     api_key='1ce5e6b52a8665b677f7a8530ced6ae2ee82f89c',
        #     response_format='json',
        #     environment=dafiti.Environment.Staging
        # )

    def ProductDeleted(self, sku):
        response = self.client.product.Get(
            SkuSellerList=[sku],
            Filter=dafiti.Filter.Deleted)

        if response.body != "" and len(response.body["Products"]) > 0:
            return True

        return False

    def ProductExist(self, sku):
        # check if product is alive
        response = self.client.product.Get(
            SkuSellerList=[sku], 
            Filter=dafiti.Filter.All)

        if response.body != "" and len(response.body["Products"]) > 0:
            return True
        else:

            # check if product was deleted
            if self.ProductDeleted(sku):
                return True

            return False

    def RemoveProduct(self, sku):
        self.client.product.Remove(sku)

    def AddProduct(self, sku, main_category, categories, color, season):
        response = None
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
                new_sku = "{}-{}".format(sku, size)

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

            # response = dafiti.Response()
            stock = self.getStock(sku, s.id)

            product_name = "{} {} {} Giani Da Firenze".format(
                p.category, p.name, p.color
            )

            if not self.ProductExist(new_sku):

                create_requests.append(
                    dafiti.ProductRequest(
                        SellerSku=new_sku, Name=self.nameFix(product_name), Description=p.description, 
                        Brand="Giani Da Firenze", Price=p.sell_price,
                        PrimaryCategory=main_category, Categories=categories.split(","),
                        Variation=size, ProductData=product_data,
                        Quantity=stock, ParentSku=sku))

            else:

                update_requests.append(
                    dafiti.ProductRequest(
                        SellerSku=new_sku, Name=self.nameFix(product_name), Description=p.description, 
                        Brand="Giani Da Firenze", Price=p.sell_price,
                        PrimaryCategory=main_category, Categories=categories.split(","),
                        Variation=size, ProductData=product_data,
                        Quantity=stock, ParentSku=sku, Status=dafiti.Status.Active))

            # save las sync
            self.insertSync(new_sku, stock)

        if len(create_requests) > 0:
            response = self.client.product.sendPOST(dafiti.EndPoint.ProductCreate, create_requests)
        if len(update_requests) > 0:
            response = self.client.product.sendPOST(dafiti.EndPoint.ProductUpdate, update_requests)

        # preparing images for dafiti
        images = [p.image, p.image_2, p.image_3, p.image_4, p.image_5, p.image_6]
        final_images = []

        for img in images:
            if img != '':
                final_images.append(
                    "http://bodegas.gianidafirenze.cl/image/dafiti/{}?mwh=1380,1160".format(img.replace(" ", "%20"))
                )

        for x in range(0,3):
            aux = final_images.pop(0)
            final_images.append(aux)

        # adding images to dafiti
        self.client.product.Image(
            image_skus,
            *final_images)

        return response

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

    def getDafitiProducts(self):
        products = self.client.product.Get(Filter=dafiti.Filter.All)
        plist = products.body["Products"]["Product"]

        if type(plist) is list:
            return plist

        return [plist]

    def syncronizeStock(self):
        """
        check each product syncrhonized with dafiti and modify stock
        """

        products = self.getDafitiProducts()
        update_requests = []

        for p in products:
            sku_seller = p["SellerSku"]
            sku = self.getSku(p["SellerSku"], p["Variation"])
            size = p["Variation"]
            size_id = Size.getSizeID(size)

            sync_stock = self.getSyncStock(sku_seller)
            stock = self.getStock(sku, size_id)
            stock_dafiti = int(p["Quantity"])

            diff_dafiti = 0
            diff_cellar = 0
            new_stock = sync_stock

            diff_dafiti = (sync_stock - stock_dafiti)
            diff_cellar = (sync_stock - stock)

            new_stock -= diff_cellar

            if diff_dafiti > 0:
                new_stock -= diff_dafiti

            if diff_cellar != 0 or diff_dafiti != 0:
                print sku
                print sync_stock, stock_dafiti, stock
                print diff_cellar, diff_dafiti
                print new_stock
                print "...................."

                if diff_dafiti > 0:
                    print "adjust bodegas"

                    kardex = Kardex()
                    c = Cellar()
                    cellar = c.GetWebCellar()

                    kardex.product_sku = sku
                    kardex.units = diff_dafiti
                    kardex.price = p["Price"]
                    kardex.size_id = size_id
                    kardex.color = p["ProductData"]["ColorNameBrand"]
                    kardex.operation_type = Kardex.OPERATION_MOV_OUT
                    kardex.user = 'dafiti@gianidafirenze.cl'
                    kardex.cellar_identifier = cellar['success']

                    res_remove = kardex.Insert()

                else:
                    print "restore"
                    new_stock = stock

                update_requests.append(
                    dafiti.ProductRequest(
                        SellerSku=sku_seller, 
                        Quantity=new_stock
                    )
                )

                # self.insertSync(sku_seller, new_stock)

        response = self.client.product.sendPOST(dafiti.EndPoint.ProductUpdate, update_requests)

        if response.type == dafiti.Response.SUCCESS:
            print "success"
            for r in update_requests:
                self.insertSync(r.SellerSku, r.Quantity)

    def getSku(self, sku, size):
        return sku.replace("-{}".format(size), "")

    def getSyncStock(self, sku):

        try:
            query = """ SELECT sync_stock 
                        FROM "Dafiti" 
                        WHERE sku = %(sku)s 
                        ORDER BY id DESC
                        LIMIT 1
                    """

            return self.execute_query(
                query,
                {
                    "sku" : sku
                })[0]["sync_stock"]
        except:
            return 0

    def insertSync(self, sku, stock):

        query = """ INSERT INTO "Dafiti" (sku, sync_stock) 
                    VALUES (%(sku)s, %(stock)s) 
                """

        params = {
            "sku" : sku,
            "stock" : stock
        }

        self.execute_query(query, params)

    def nameFix(self, name):
        """
        return a capitalized version of name
        @name <String> name of product
        @sample  name="zapato ROJO"
        @return "Zapato Rojo"
        """
        sentence = name.split(" ")
        new_sentence = []

        for word in sentence:
            new_sentence.append(word.lower().capitalize())

        return " ".join(new_sentence).encode('UTF-8').strip()
