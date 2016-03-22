#!/usr/bin/python
# -*- coding: UTF-8 -*-

import dafiti
import json
import time

from lp.globals import *
from src.model10.product import Product
from src.model10.dafitimodel import DafitiModel
from tornado.options import define, options

if "enviroment" not in options:

    print enviroment

    define("enviroment", default=enviroment, type=str)
    define("db_name", default=DB_NAME, help="", type=str)
    define("db_user", default=DB_USER, help="", type=str)
    define("db_host", default=DB_HOST, help="", type=str)
    define("db_password", default=DB_PASSWORD, help="", type=str)


def GetSeason(category_name):
    categories = {
        'Botin': 'invierno',
        'Bota': 'invierno',
        'Zapatilla': 'verano', 
        'Zapato': 'invierno', 
        '2': 'invierno', 
        'Test': 'invierno', 
        'Sandalia': 'verano', 
        'Bot\xc3\xadn': 'invierno'
    }

    try:
        return categories[category_name]
    except:
        return 'invierno'


def GetCategories(category_name):
    categories = {
        'Botin': '148',
        'Bota': '514',
        'Zapatilla': '48,49', 
        'Zapato': '152', 
        '2': False, 
        'Test': False, 
        'Sandalia': '17', 
        'Bot\xc3\xadn': '148'
    }

    try:
        return categories[category_name]
    except:
        return False


def GetColor(color_name):
    colors = {
        "Café Azul Print": "Azul",
        "camel": "Marrón",
        "Café Print Negro": "Negro",
        "Café Militar": "Marrón",
        "Croco Café Cobre": "Marrón",
        "Negro Croco Camuflaje Gris": "Negro",
        "Negro Beige": "Negro",
        "Azul Print Café": "Azul",
        "Negro": "Negro",
        "Rojo Azul Blanco": "Rojo",
        "Camel Dorado": "Marrón",
        "Verde Musgo Café": "Verde",
        "Café Beige": "Beige",
        "Azul Serpiente Plata": "Azul",
        "beige taupe232323": "Beige",
        "Verdes": "Verde",
        "Café Naranjo Print": "Naranjo",
        "Café Croco Café": "Marrón",
        "café negro": "Negro",
        "Coral Print Negro": "Negro",
        "Verde Naranjo Camel": "Naranjo",
        "Negro Dorado Negro": "Negro",
        "Caramelo Mimbre Calipso": "Verde",
        "Coral Serpiente Negro": "Negro",
        "Camel Flores": "Marrón",
        "Rojo": "Rojo",
        "camel rojo": "Rojo",
        "Negro Gris": "Gris",
        "Camel Café Croco": "Marrón",
        "Azul Leopardo Natural": "Azul",
        "Croco Negro": "Negro",
        "Camel Café": "Marrón",
        "Camuflaje Café Verde Negro": "Verde",
        "camel azul": "Azul",
        "Café Verde": "Verde",
        "Beige": "Beige",
        "Camel Croco Caramelo": "Marrón",
        "Azul": "Azul",
        "Cerámico Serpiente Beige": "Beige",
        "beige": "Beige",
        "Fucsia Verde Flores": "Fucsia",
        "Café Croco Beige": "Beige",
        "Print Café Beige Negro": "Negro",
        "Verde Negro Serpiente": "Verde",
        "rosa viejo": "Rosa",
        "negro camello": "Negro",
        "Negro Camuflaje Gris": "Negro",
        "Print Negro": "Negro",
        "Azul Verde Serpiente": "Verde",
        "Croco Rojo": "Rojo",
        "Croco Beige": "Beige",
        "azul café": "Azul",
        "Naranja Leopardo": "Naranja",
        "café beige": "Beige",
        "mostaza": "Mostaza",
        "café": "Marrón",
        "café moro": "Marrón",
        "Verde Café": "Verde",
        "negro": "Negro",
        "verde": "Verde",
        "Reno Negro Cebra": "Negro",
        "Taupe": "Taupe",
        "Azul Fucsia Multicolor": "Fucsia",
        "croco beige": "Beige",
        "Musgo": "Verde",
        "Café Negro": "Negro",
        "Café Chocolate": "Chocolate",
        "Rojo Croco Rojo": "Rojo",
        "camel café": "Marrón",
        "Vison": "Marrón",
        "Camel Serpiente": "Camel",
        "Verde Beige Café": "Verde",
        "croco negro gris": "Negro",
        "azul": "Azul",
        "café gris": "Gris",
        "Café": "Marrón",
        "Negro Croco": "Negro",
        "Negro Azul": "Azul",
        "Naranjo": "Naranjo",
        "Amarilla": "Amarillo",
        "Galleta Reptil Rojo": "Rojo",
        "musgo": "Verde",
        "Negro Sepiente Plateado": "Negro",
        "Naranjo Print Café": "Naranjo",
        "Verde Serpiente Negro": "Verde",
        "Croco Beige Verde Oscuro": "Beige",
        "café verde": "Verde",
        "verde gris": "Verde",
        "Caramelo Fantasia": "Rojo",
        "Croco Beige Taupe": "Beige",
        "verde beige": "Verde",
        "café ocre": "Marrón",
        "croco rojo": "Rojo",
        "Azul Negro": "Azul",
        "Negro Café": "Marrón",
        "Camel": "Marrón",
        "Café Negro Charol": "Negro",
        "Azul Print Negro": "Azul",
        "Café Verde Musgo": "Verde"
    }

    try:
        return colors[color_name]
    except:
        return 'Negro'


def main():

    products = Product().GetList(items=400)["success"]

    d = DafitiModel()

    for p in products:

        category = GetCategories(p["category"])
        color = GetColor(p["color"])
        season = GetSeason(p["category"])

        if category:
            try:
                print "adding:", p["sku"]
                print p["category"], category
                print p["color"], color
                print season

                r = d.AddProduct(p["sku"], category.split(",")[0], category, color, season)

                if r.type == dafiti.Response.ERROR:
                    print "    error:", r.head
            except Exception, e:
                print "     ex: " + str(e)
            time.sleep(120)


if __name__ == "__main__":

    main()
