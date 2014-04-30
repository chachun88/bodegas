'''
Created on 13/12/2012

@author: ricardo

Jueves 12 dic 2012

reutilizado por chinostroza en tellmecuando
'''

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

token = "5334d6c29ec9a710f56d9ab5"
#webservice_url = "http://giani.loadingplay.com:8888"
webservice_url = "http://localhost:8888"

facebookimage="http://tellmecuando.com/static/img/logo_slogan2.png"
debugMode = True
port = 9003
if (debugMode):
    userMode="test"
    carpeta_img = 'C:\Python27\tellmecuando\static\img'
else:
    userMode="prod"
    carpeta_img = '/var/www/tellmecuando/static/img'

carpeta_app = '/var/www/tellmecuando'
pp_url = "https://www.puntopagos.com"
pp_secret = "HoXTD8Ds4EiaBOce87wylKZyGiyXPKoyOP57O8uV"
pp_key = "dTtvpp4D3uTy8AuC2gMR"

if (debugMode):
    port = 9003
else:
    port = 9003
    
if (debugMode):
    domainName = "tellmecuando.loadingplay.com";
else:
    domainName = "www.tellmecuando.com";

    
if(debugMode):
    pp_url = "http://sandbox.puntopagos.com"
    pp_secret = "i2n5wRw1w99kGPhnwLSk9wWC117clhTllH6E2Fgv"
    pp_key = "4gCE2c2PClMRrDRsZpct"
else:
    pp_url = "https://www.puntopagos.com"
    pp_secret = "HoXTD8Ds4EiaBOce87wylKZyGiyXPKoyOP57O8uV"
    pp_key = "dTtvpp4D3uTy8AuC2gMR"
    
if(debugMode):
    carpeta_app = '/var/www/tellmecuando.loadingplay.com'
else:
    carpeta_app = '/var/www/tellemecuando'

class Menu:

    PRODUCTOS = "Productos"

    # sub_menu
    PRODUCTOS_CARGA_MASIVA = "Carga Masiva"
    PRODUCTOS_SALIDA_MASIVA = "Salida Masiva"
    PRODUCTOS_CARGA = "Agregar producto"
    PRODUCTOS_LISTA = "Lista de productos"
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

    INFORMES = "Informes"

    # sub_menu
    INFORMES_POR_BODEGA = "Informe por bodega"
    # end sub_menu

    SALIR = "Salir"