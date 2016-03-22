#!/usr/bin/python
# -*- coding: UTF-8 -*-

import dafiti

# -------------------

from lp.globals import *
from src.model10.dafitimodel import DafitiModel
from tornado.options import define, options

if "enviroment" not in options:

    print enviroment

    define("enviroment", default=enviroment, type=str)
    define("db_name", default=DB_NAME, help="", type=str)
    define("db_user", default=DB_USER, help="", type=str)
    define("db_host", default=DB_HOST, help="", type=str)
    define("db_password", default=DB_PASSWORD, help="", type=str)

# -------------------


if __name__ == "__main__":

    model = DafitiModel()
    client = dafiti.API(
            user_id='contacto@gianidafirenze.cl',
            api_key='aa8051656b6b1efab5b52615e2e4e2fe913b13d7',
            response_format='json',
            environment=dafiti.Environment.Live
        )

    response = client.product.Get(Filter=dafiti.Filter.All)

    counter_a = 0
    counter_b = 0

    requests = []
    product_request = []

    for p in response.body["Products"]["Product"]:
        name_fixed = model.nameFix(p["Name"])
        counter_a += 1

        if p["Name"] != name_fixed:

            product_request.append(dafiti.ProductRequest(
                    SellerSku=p["SellerSku"],
                    Name=name_fixed
                ))

            if len(product_request) >= 50:
                requests.append(product_request)
                product_request = []

            counter_b += 1

    if len(product_request) > 0:
        requests.append(product_request)

    for r in requests:
        response = client.product.sendPOST(dafiti.EndPoint.ProductUpdate, r)
        print response.head

    print counter_a, counter_b
