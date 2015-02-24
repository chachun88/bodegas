'''
Created on 13/12/2012

@author: ricardo

Jueves 12 dic 2012

reutilizado por chinostroza en tellmecuando
reutilizado por estefy en bodegas
'''

import os

if os.name == "nt":
    debugMode = True
else:
    debugMode = False

token = "5334d6c29ec9a710f56d9ab5"
webservice_url = "http://localhost"
port = 0
ws_port = 0

BODEGA_PORT = 9007
WS_PORT = 8890
BODEGA_DEBUG_PORT = 9008
DEBUG_WS_PORT = 8891


print "debug mode enabled : {}".format(debugMode)


# setting vars
if (debugMode):
    userMode = "test"
    port = BODEGA_DEBUG_PORT
    ws_port = DEBUG_WS_PORT
else:
    userMode = "prod"
    port = BODEGA_PORT
    ws_port = WS_PORT


webservice_url += ":{}".format(ws_port)


# --- menu ---
class Menu:

    INFORMES = "Informes"

    # sub_menu
    INFORMES_POR_BODEGA = "Informe por bodega"
    # end sub_menu

    PRODUCTOS = "Productos"

    # sub_menu
    PRODUCTOS_CARGA_MASIVA = "Carga Masiva"
    PRODUCTOS_SALIDA_MASIVA = "Salida Masiva"
    PRODUCTOS_CARGA = "Agregar producto"
    PRODUCTOS_LISTA = "Maestro productos"
    # end sub_menu

    BODEGAS = "Bodegas"

    # sub_menu 
    BODEGAS_LISTAR = "Lista de bodegas"
    BODEGAS_AGREGAR = "Agregar bodega"
    # end sub_menu

    USUARIOS = "Usuarios"

    # sub_menu
    USUARIOS_LISTAR = "Lista de usuarios"
    USUARIOS_AGREGAR = "Agregar usuario"
    # sub_menu

    SALIR = "Salir"


# --- functions ---
def tomoney(x):
    if x != "":
        flotante = '{:20,.0f}'.format(float(x))
        price = flotante.replace(",",".")
        return "$"+price.strip()
    else:
        return ""


def roundfloat(x):
    flotante = ("{0:.0f}".format(round(x,2)))
    price = flotante.replace(",",".")
    return price.strip() 
