#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from src.model.address import Address
from src.model.user import User
from src.model.globals import *
from src.model.user_address import User_Address
from src.model.enterprise import Enterprise
from src.model.enterprise_address import Enterprise_Address
from datetime import datetime


class ModelAddressTest(unittest.TestCase):
    """docstring for ModelAddressTest"""

    def setUp(self):
        self.address = Address()

    def tearDown(self):
        self.address.clear()

    def test_save(self):

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert alias",
                "result" : {}
            }
        )

        self.address.alias = "mi casa"

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert address",
                "result" : {}
            }
        )

        self.address.address = "alonso de cordova"

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert town",
                "result" : {}
            }
        )

        self.address.town = '1'

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "town must be an integer",
                "result" : {}
            }
        )

        self.address.town = 1

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert city",
                "result" : {}
            }
        )

        self.address.city = '1'

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "city must be an integer",
                "result" : {}
            }
        )

        self.address.city = 1

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert state",
                "result" : {}
            }
        )

        self.address.state = '1'

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "state must be an integer",
                "result" : {}
            }
        )

        self.address.state = 1

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert country",
                "result" : {}
            }
        )

        self.address.country = '1'

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : VALIDATION_CODE,
                "message" : "country must be an integer",
                "result" : {}
            }
        )

        self.address.country = 1

        self.assertDictEqual(
            self.address.save(),
            {
                "state" : SUCCESS_CODE,
                "message" : "address create successfully",
                "result" : {"identifier": 1}
            }
        )

    def text_init(self):

        address = Address()
        address.alias = "mi oficina"
        address.city = 1
        address.town = 1
        address.country = 1
        address.address = "encomnderos"
        address.state = 1
        identifier = address.save()["result"]["identifier"]

        self.assertDictEqual(
            self.address.initById(identifier)["result"],
            {
                "identifier": 1,
                "alias": "mi oficina",
                "city": 1,
                "town": 1,
                "country": 1,
                "address": "encomnderos",
                "state": 1
            }
        )

    def test_edit(self):

        address = Address()
        address.alias = "mi oficina"
        address.city = 1
        address.town = 1
        address.country = 1
        address.address = "encomnderos"
        address.state = 1
        identifier = address.save()["result"]["identifier"]

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert identifier",
                "result" : {}
            }
        )

        self.address.identifier = '1'

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "identifier must be an integer",
                "result" : {}
            }
        )

        self.address.identifier = identifier

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert alias",
                "result" : {}
            }
        )

        self.address.alias = 'mi casa'

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert address",
                "result" : {}
            }
        )

        self.address.address = "buenaventura 3268"

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert town",
                "result" : {}
            }
        )

        self.address.town = '1'

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "town must be an integer",
                "result" : {}
            }
        )

        self.address.town = 1

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert city",
                "result" : {}
            }
        )

        self.address.city = '1'

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "city must be an integer",
                "result" : {}
            }
        )

        self.address.city = 1

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert state",
                "result" : {}
            }
        )

        self.address.state = '1'

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "state must be an integer",
                "result" : {}
            }
        )

        self.address.state = 1

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "please insert country",
                "result" : {}
            }
        )

        self.address.country = '1'

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : VALIDATION_CODE,
                "message" : "country must be an integer",
                "result" : {}
            }
        )

        self.address.country = 1

        self.assertDictEqual(
            self.address.edit(),
            {
                "state" : SUCCESS_CODE,
                "message" : "address has been successfully updated",
                "result" : {"identifier": 1}
            }
        )

        self.assertDictEqual(
            self.address.initById(identifier),
            {
                "state": SUCCESS_CODE,
                "message": "get address by identifier, ok",
                "result": {
                    "alias" : "mi casa",
                    "city" : 1,
                    "town" : 1,
                    "country" : 1,
                    "address" : "buenaventura 3268",
                    "state" : 1,
                    "identifier" : identifier
                }
            }
        )

    def test_list_customer(self):

        user = User()
        user.name = "Ricardo"
        user.email = "ricardo@loadingplay.com"
        user.phone = ""
        user.last_name = "Silva"
        user.password = "1234"
        user.create()

        address = Address()
        address.alias = "mi oficina"
        address.city = 1
        address.town = 1
        address.country = 1
        address.address = "encomnderos"
        address.state = 1
        identifier = address.save()["result"]["identifier"]

        user_address = User_Address()
        user_address.user_id = user.identifier
        user_address.address_id = identifier
        user_address.save()

        address1 = Address()
        address1.alias = "mi casa"
        address1.city = 1
        address1.town = 3
        address1.country = 1
        address1.address = "buenaventura"
        address1.state = 1
        identifier1 = address1.save()["result"]["identifier"]

        user_address = User_Address()
        user_address.user_id = user.identifier
        user_address.address_id = identifier1
        user_address.save()

        self.maxDiff = None

        self.assertDictEqual(self.address.listByCustomerId(user.identifier),{
                "state": SUCCESS_CODE,
                "message": "list address by user identifier is ok",
                "result": [{
                    "identifier": 1,
                    "alias": "mi oficina",
                    "city": 1,
                    "town": 1,
                    "country": 1,
                    "address": "encomnderos",
                    "state": 1
                }, {
                    "identifier": 2,
                    "alias": "mi casa",
                    "city": 1,
                    "town": 3,
                    "country": 1,
                    "address": "buenaventura",
                    "state": 1
                }]
            }
        )

    def test_list_enterprise(self):

        enterprise = Enterprise()
        enterprise.name = "Wait for it"
        enterprise.bussiness = "informática"
        enterprise.rut = "167618979"
        enterprise.status = Enterprise.ESTADO_ACEPTADO
        enterprise.approval_date = '2015-02-12 12:00:00'
        enterprise.registration_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        enterprise.deleted = False
        enterprise.save()

        address = Address()
        address.alias = "mi oficina"
        address.city = 1
        address.town = 1
        address.country = 1
        address.address = "encomnderos"
        address.state = 1
        identifier = address.save()["result"]["identifier"]

        enterprise_address = Enterprise_Address()
        enterprise_address.enterprise_id = enterprise.identifier
        enterprise_address.address_id = identifier
        enterprise_address.save()

        address1 = Address()
        address1.alias = "mi casa"
        address1.city = 1
        address1.town = 3
        address1.country = 1
        address1.address = "buenaventura"
        address1.state = 1
        identifier1 = address1.save()["result"]["identifier"]

        enterprise_address = Enterprise_Address()
        enterprise_address.enterprise_id = enterprise.identifier
        enterprise_address.address_id = identifier1
        enterprise_address.save()

        self.maxDiff = None

        self.assertDictEqual(self.address.listByEnterpriseId(enterprise.identifier),{
                "state": SUCCESS_CODE,
                "message": "list address by enterprise identifier is ok",
                "result": [{
                    "identifier": 1,
                    "alias": "mi oficina",
                    "city": 1,
                    "town": 1,
                    "country": 1,
                    "address": "encomnderos",
                    "state": 1
                }, {
                    "identifier": 2,
                    "alias": "mi casa",
                    "city": 1,
                    "town": 3,
                    "country": 1,
                    "address": "buenaventura",
                    "state": 1
                }]
            }
        )
