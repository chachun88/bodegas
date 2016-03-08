#!/usr/bin/python
# -*- coding: UTF-8 -*-

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


def job():
    dafiti = DafitiModel()
    dafiti.syncronizeStock()


if __name__ == "__main__":
    # while True:
    job()
    # time.sleep(10)
