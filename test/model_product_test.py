#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from src.model10.product import Product
from src.model10.tag import Tag
from datetime import datetime
from lp.model.basemodel import BaseModel


class ModelProductTest(unittest.TestCase):
    """docstring for ModelAddressTest"""

    def setUp(self):
        self.product = Product()

    def tearDown(self):
        BaseModel.execute_query( '''TRUNCATE "Product" CASCADE;''' )

    def test_save(self):

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

        self.product.name = 'Queltehue 19'
        self.product.sku = 'GDF-OI14-Queltehue-C19-'
        self.product.descripction = 'descripcion'
        self.product.brand = 'Giani Da Firenze'
        self.product.manufacturer = 'Calzur'
        self.product.size = ['35', '36', '37']
        self.product.color = 'café moro'
        self.product.bullet_1 = ''
        self.product.bullet_2 = ''
        self.product.bullet_3 = ''
        self.product.currency = 'CLP'
        self.product.image = ''
        self.product.image_2 = ''
        self.product.image_3 = ''
        self.product.image_4 = ''
        self.product.image_5 = ''
        self.product.image_6 = ''
        self.product.category = ''
        self.product.upc = ''
        self.product.price = 33558
        self.product.sell_price = 0
        self.product.delivery = 'delivery'
        self.product.which_size = 'qureywe'
        self.product.tags = ','.join([str(identificador) for identificador in tags])
        self.product.promotion_price = 0
        self.product.size_id = [1, 27, 28]
        self.product.bulk_price = 0

        self.assertDictEqual({
            "success": "product correctly inserted"
            }, self.product.Save()
        ) 
