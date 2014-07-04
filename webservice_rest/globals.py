'''
Created on 13/12/2012

@author: ricardo

Jueves 12 dic 2012

reutilizado por chinostroza en tellmecuando
reutilizado por estefy en bodegas
'''

import os


debugMode = False

token = "5334d6c29ec9a710f56d9ab5"
webservice_url = "http://localhost"
port = 0
ws_port = 0


### reading config file
if os.name == "posix":
    config_file = open("../CONFIG.txt", "r")
else:
    config_file = open("C:\\Users\\Estefi\\Desktop\\git\\bodegas\\CONFIG.txt", "r")

config_data = config_file.read()

config = {}

for x in config_data.split("\n"):

    sp = x.split("=")
    key = sp[0]
    val = sp[1]

    config[key] = val


print "debug mode enabled : " + config["DEBUG"] 

### setting config values
if config["DEBUG"] == "True":
    debugMode = True

### setting vars
if (debugMode):
    userMode="test"
    carpeta_img = 'C:\Python27\tellmecuando\static\img'
else:
    userMode="prod"
    carpeta_img = '/var/www/tellmecuando/static/img'


if (debugMode):
    port = config["DEBUG_PORT"]
    ws_port = config["DEBUG_WS_PORT"]
else:
    port = config["PORT"]
    ws_port = config["WS_PORT"]

webservice_url += ":" + ws_port


#### menu #####

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


#### functions #####
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
