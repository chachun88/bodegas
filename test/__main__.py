#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from src.model10.dafitimodel import DafitiModel

from config import *
from tornado.options import define
from lp.globals import Enviroment

define("protocol", default="https", help="run on the given port", type=str)

define("enviroment", default=Enviroment.ONTEST, type=str)
define("db_name", default=ONTEST_DB_NAME, help="", type=str)
define("db_user", default=ONTEST_USER, help="", type=str)
define("db_host", default=ONTEST_HOST, help="", type=str)
define("db_password", default=ONTEST_PASSWORD, help="", type=str)

# from model_kardex_test import ModelKardexTest
# from handler_kardex_test import TestStock


class DafitiTestCase(unittest.TestCase):

    def setUp(self):
        self.dafiti = DafitiModel()

    def test_add_sync_stock(self):

        self.dafiti.insertSync("foo", 10)
        self.assertEqual(self.dafiti.checkStock("foo"), 10)

        self.dafiti.insertSync("foo", 5)
        self.assertEqual(self.dafiti.checkStock("foo"), 5)

        self.assertEqual(self.dafiti.checkStock("nonexistent"), 0)

if __name__ == '__main__': 
    unittest.main() 
