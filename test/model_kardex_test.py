#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from src.model10.kardex import Kardex
from src.model10.product import Product
from src.model10.tag import Tag
from src.model10.cellar import Cellar
from src.model10.size import Size
from src.model10.city import City
from lp.model.basemodel import BaseModel


class ModelKardexTest(unittest.TestCase):
    """docstring for ModelAddressTest"""

    def setUp(self):
        self.kardex = Kardex()

    def tearDown(self):
        BaseModel.execute_query( '''TRUNCATE "Kardex" CASCADE;''' )

    def test_add(self):

        city = City()
        city.name = "Santiago"
        city.Save()

        cellar = Cellar()
        cellar.city = city.id
        cellar.name = 'Bodega Central'
        res = cellar.Save()

        tags = []

        tag = Tag()
        tag.name = 'botin'
        res = tag.Save()

        if "success" in res:
            tags.append(res["success"])

        tag.name = 'queltehue'
        res = tag.Save()

        if "success" in res:
            tags.append(res["success"])

        size = Size()
        size.name = '35'
        res = size.insert()

        size_id = []

        if "success" in res:
            size_id.append(size.id)

        size = Size()
        size.name = '36'
        res = size.insert()

        if "success" in res:
            size_id.append(size.id)

        size = Size()
        size.name = '37'
        res = size.insert()

        if "success" in res:
            size_id.append(size.id)

        product = Product()

        product.name = 'Queltehue 19'
        product.sku = 'GDF-OI14-Queltehue-C19'
        product.descripction = 'descripcion'
        product.brand = 'Giani Da Firenze'
        product.manufacturer = 'Calzur'
        product.size = ['35', '36', '37']
        product.color = 'café moro'
        product.bullet_1 = ''
        product.bullet_2 = ''
        product.bullet_3 = ''
        product.currency = 'CLP'
        product.image = ''
        product.image_2 = ''
        product.image_3 = ''
        product.image_4 = ''
        product.image_5 = ''
        product.image_6 = ''
        product.category = ''
        product.upc = ''
        product.price = 33558
        product.sell_price = 0
        product.delivery = 'delivery'
        product.which_size = 'qureywe'
        product.tags = ','.join([str(identificador) for identificador in tags])
        product.promotion_price = 0
        product.size_id = size_id
        product.bulk_price = 0

        product.Save()

        self.kardex.product_sku = 'GDF-OI14-Queltehue-C19'
        self.kardex.units = 3
        self.kardex.price = product.price
        self.kardex.cellar_identifier = cellar.id
        self.kardex.color = product.color
        self.kardex.operation_type = Kardex.OPERATION_BUY
        self.kardex.size_id = size_id[0]

        self.assertDictEqual(
            {
                "success": "products has been added"
            }, self.kardex.Insert()
        )   

    def test_remove(self):

        city = City()
        city.name = "Santiago"
        city.Save()

        cellar = Cellar()
        cellar.city = city.id
        cellar.name = 'Bodega Central'
        res = cellar.Save()

        tags = []

        tag = Tag()
        tag.name = 'botin'
        res = tag.Save()

        if "success" in res:
            tags.append(res["success"])

        tag.name = 'queltehue'
        res = tag.Save()

        if "success" in res:
            tags.append(res["success"])

        size = Size()
        size.name = '35'
        res = size.insert()

        size_id = []

        if "success" in res:
            size_id.append(size.id)

        size = Size()
        size.name = '36'
        res = size.insert()

        if "success" in res:
            size_id.append(size.id)

        size = Size()
        size.name = '37'
        res = size.insert()

        if "success" in res:
            size_id.append(size.id)

        product = Product()

        product.name = 'Queltehue 19'
        product.sku = 'GDF-OI14-Queltehue-C19'
        product.descripction = 'descripcion'
        product.brand = 'Giani Da Firenze'
        product.manufacturer = 'Calzur'
        product.size = ['35', '36', '37']
        product.color = 'café moro'
        product.bullet_1 = ''
        product.bullet_2 = ''
        product.bullet_3 = ''
        product.currency = 'CLP'
        product.image = ''
        product.image_2 = ''
        product.image_3 = ''
        product.image_4 = ''
        product.image_5 = ''
        product.image_6 = ''
        product.category = ''
        product.upc = ''
        product.price = 33558
        product.sell_price = 0
        product.delivery = 'delivery'
        product.which_size = 'qureywe'
        product.tags = ','.join([str(identificador) for identificador in tags])
        product.promotion_price = 0
        product.size_id = size_id
        product.bulk_price = 0

        product.Save()

        self.kardex.product_sku = 'GDF-OI14-Queltehue-C19'
        self.kardex.units = 3
        self.kardex.price = product.price
        self.kardex.cellar_identifier = cellar.id
        self.kardex.color = product.color
        self.kardex.operation_type = Kardex.OPERATION_BUY
        self.kardex.size_id = size_id[0]

        new_kardex = Kardex()
        new_kardex.product_sku = 'GDF-OI14-Queltehue-C19'
        new_kardex.units = 2
        new_kardex.sell_price = 69900
        new_kardex.cellar_identifier = cellar.id
        new_kardex.color = product.color
        new_kardex.operation_type = Kardex.OPERATION_SELL
        new_kardex.size_id = size_id[0]

        self.assertDictEqual(
            {
                "success": "products has been added"
            }, self.kardex.Insert()
        )

    def test_mov(self):

        city = City()
        city.name = "Santiago"
        city.Save()

        cellar = Cellar()
        cellar.city = city.id
        cellar.name = 'Bodega Central'
        res = cellar.Save()

        new_cellar = Cellar()
        new_cellar.city = city.id
        new_cellar.name = 'Bodega Reserva'
        res = new_cellar.Save()

        tags = []

        tag = Tag()
        tag.name = 'botin'
        res = tag.Save()

        if "success" in res:
            tags.append(res["success"])

        tag.name = 'queltehue'
        res = tag.Save()

        if "success" in res:
            tags.append(res["success"])

        size = Size()
        size.name = '35'
        res = size.insert()

        size_id = []

        if "success" in res:
            size_id.append(size.id)

        size = Size()
        size.name = '36'
        res = size.insert()

        if "success" in res:
            size_id.append(size.id)

        size = Size()
        size.name = '37'
        res = size.insert()

        if "success" in res:
            size_id.append(size.id)

        product = Product()
        product.name = 'Queltehue 19'
        product.sku = 'GDF-OI14-Queltehue-C19'
        product.descripction = 'descripcion'
        product.brand = 'Giani Da Firenze'
        product.manufacturer = 'Calzur'
        product.size = ['35', '36', '37']
        product.color = 'café moro'
        product.bullet_1 = ''
        product.bullet_2 = ''
        product.bullet_3 = ''
        product.currency = 'CLP'
        product.image = ''
        product.image_2 = ''
        product.image_3 = ''
        product.image_4 = ''
        product.image_5 = ''
        product.image_6 = ''
        product.category = ''
        product.upc = ''
        product.price = 33558
        product.sell_price = 0
        product.delivery = 'delivery'
        product.which_size = 'qureywe'
        product.tags = ','.join([str(identificador) for identificador in tags])
        product.promotion_price = 0
        product.size_id = size_id
        product.bulk_price = 0

        product.Save()

        self.kardex.product_sku = 'GDF-OI14-Queltehue-C19'
        self.kardex.units = 3
        self.kardex.price = product.price
        self.kardex.cellar_identifier = cellar.id
        self.kardex.color = product.color
        self.kardex.operation_type = Kardex.OPERATION_MOV_OUT
        self.kardex.size_id = size_id[0]

        new_kardex = Kardex()
        new_kardex.product_sku = 'GDF-OI14-Queltehue-C19'
        new_kardex.units = 2
        self.kardex.price = product.price
        new_kardex.cellar_identifier = new_cellar.id
        new_kardex.color = product.color
        new_kardex.operation_type = Kardex.OPERATION_MOV_IN
        new_kardex.size_id = size_id[0]

        self.assertDictEqual(
            {
                "success": "products has been added"
            }, self.kardex.Insert()
        )
