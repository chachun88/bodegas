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

testMode = True

BODEGA_PORT = 9007
WS_PORT = 8890
BODEGA_DEBUG_PORT = 9008
DEBUG_WS_PORT = 8891

appid = 100

webservice_url = "http://localhost"
port = 0
ws_port = 0

reserve_cellar_id = 12
email_giani = "contacto@gianidafirenze.cl"

# setting vars
if (debugMode):
    userMode = "test"
    carpeta_img = 'C:\Python27\tellmecuando\static\img'
    port = BODEGA_DEBUG_PORT
    ws_port = DEBUG_WS_PORT
    webservice_url += ":{}".format(ws_port)
elif testMode:
    userMode = "test"
    carpeta_img = 'C:\Python27\tellmecuando\static\img'
    port = BODEGA_PORT
    ws_port = WS_PORT
    webservice_url = "http://wgiani.ondev.today"
else:
    userMode = "prod"
    carpeta_img = '/var/www/tellmecuando/static/img'
    port = BODEGA_PORT
    ws_port = WS_PORT
    webservice_url = "http://wgiani.loadingplay.com"


# --- menu ---

class Menu:

    INFORMES = "Informes"

    # sub_menu
    INFORMES_POR_BODEGA = "Informe por bodega"
    # end sub_menu

    PRODUCTOS = "Productos"

    # sub_menu
    PRODUCTOS_CARGA_MASIVA = "Carga masiva"
    PRODUCTOS_SALIDA_MASIVA = "Salida masiva"
    PRODUCTOS_CARGA = "Agregar producto"
    PRODUCTOS_LISTA = "Maestro productos"
    # end sub_menu

    BODEGAS = "Bodegas"

    # sub_menu 
    BODEGAS_LISTAR = "Lista de bodegas"
    BODEGAS_AGREGAR = "Agregar bodega"
    BODEGAS_FORSALE = "Seleccionar bodega web"
    BODEGAS_RESERVATION = "Seleccionar bodega de reserva online"
    # end sub_menu

    USUARIOS = "Usuarios"

    # sub_menu
    USUARIOS_LISTAR = "Lista de usuarios"
    USUARIOS_AGREGAR = "Agregar usuario"
    # sub_menu

    PEDIDOS = "Pedidos"

    # sub_menu 
    PEDIDOS_LISTA = "Lista de pedidos"
    # end sub_menu

    CLIENTES = "Clientes"

    # sub_menu 
    CLIENTES_LISTAR = "Lista de clientes"
    # end sub_menu

    TAGS = "Tags"
    TAGS_LISTAR = "Lista de Tags"
    TAGS_ADD = "Agregar tag"

    SHIPPING = "Despacho"
    SHIPPING_LIST = "Lista de precios"
    SHIPPING_SAVE = "Agregar precio"

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
