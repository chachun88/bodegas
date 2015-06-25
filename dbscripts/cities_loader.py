#!/usr/bin/python
# -*- coding: UTF-8 -*-
from src.model10.city import City
from src.model10.shipping import Shipping
from lp.model.basemodel import BaseModel
from tornado.options import define

import xlrd  # lib excel

from config import *

define("db_name", default=LOCAL_DB_NAME, help="", type=str)
define("db_user", default=LOCAL_USER, help="", type=str)
define("db_host", default=LOCAL_HOST, help="", type=str)
define("db_password", default=LOCAL_PASSWORD, help="", type=str)

query = '''select id from "City" where lower(name) = %(name)s'''
parameters = {
    "name": 'santiago'
}

from_city_id = None

try:
    from_city_id = BaseModel.execute_query_real(query, parameters)[0]['id']
except Exception, e:
    print str(e)

doc = xlrd.open_workbook('dbscripts/comunas.xls')

sheet = doc.sheet_by_index(0)

nrows = sheet.nrows
ncols = sheet.ncols

# fila (empieza con 1)
for i in range(1, nrows):

    city = City()
    shipping = Shipping()

    # columna
    for j in range(ncols):

        if j == 2:
            value = sheet.cell_value(i, j)
            if value != '':
                comuna = value.lower()
                city.name = comuna
                response = city.Save()

                if "error" in response:
                    print response['error']

        if j == 6:
            value = sheet.cell_value(i, j)

            if value != '':
                precio = int(value)
                shipping.identifier = ''
                shipping.from_city_id = from_city_id
                shipping.to_city_id = city.id
                shipping.correos_price = 0
                shipping.chilexpress_price = precio
                shipping.price = precio
                shipping.edited = False
                shipping.charge_type = 1
                response = shipping.Save()

                # print response

                if "error" in response:
                    print response['error']
