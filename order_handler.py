#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from globals import Menu

from basehandler import BaseHandler
from model.order import Order
from model.product import Product

from datetime import datetime

from bson import json_util

ACCIONES_ELIMINAR = 1
ACCIONES_CONFIRMAR = 2
ACCIONES_PICKING = 3
ACCIONES_DESPACHADO = 4
ACCIONES_CANCELADO = 5

ESTADO_PENDIENTE = 1
ESTADO_CONFIRMADO = 2
ESTADO_PICKING = 3
ESTADO_DESPACHADO = 4
ESTADO_CANCELADO = 5

class OrderHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.PEDIDOS_LISTA)

        order = Order()
        pedidos = order.List()
        self.render("order/home.html",side_menu=self.side_menu, pedidos=pedidos, dn=self.get_argument("dn", ""))

class AddOrderHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        order = Order()
        self.render("order/save.html",dn="",mode="add", order=order)

    @tornado.web.authenticated
    def post(self):

        # instantiate order
        order = Order()

        order.id                = self.get_argument("id", "")
        order.date              = datetime.now()
        order.salesman          = self.get_argument("salesman", "")
        order.customer          = self.get_argument("customer", "")
        order.subtotal          = self.get_argument("subtotal", "")
        order.discount          = self.get_argument("discount", "")
        order.tax               = self.get_argument("tax", "")
        order.total             = self.get_argument("total", "")
        order.address           = self.get_argument("address", "")
        order.town              = self.get_argument("town", "")
        order.city              = self.get_argument("city", "")
        order.country           = self.get_argument("country","")
        order.type              = self.get_argument("type","")
        order.source            = self.get_argument("source","")
        order.items_quantity    = self.get_argument("items_quantity","")
        order.product_quantity  = self.get_argument("product_quantity","")
        order.state             = self.get_argument("state","")

        #saving the current order
        oid = order.Save()

        self.write(oid)

class OrderActionsHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self):

        order=Order()

        valores = self.get_argument("values","")
        accion = self.get_argument("action","")

        if accion == "":
            self.write("Debe seleccionar una acción")
            return 

        accion = int(accion)

        if valores == "":
            self.write("Debe seleccionar al menos un pedido")
            return

        if accion == ACCIONES_ELIMINAR:

            response = order.Remove(valores)

            self.write(json_util.dumps(response))

        elif accion == ACCIONES_CONFIRMAR:
            
            response = order.ChangeStateOrders(valores,ESTADO_CONFIRMADO)
            
            self.write(json_util.dumps(response))

        elif accion == ACCIONES_PICKING:

            response = order.ChangeStateOrders(valores,ESTADO_PICKING)

            self.write(json_util.dumps(response))

        elif accion == ACCIONES_DESPACHADO:

            response = order.ChangeStateOrders(valores,ESTADO_DESPACHADO)

            self.write(json_util.dumps(response))

        elif accion == ACCIONES_CANCELADO:

            response = order.ChangeStateOrders(valores,ESTADO_CANCELADO)

            self.write(json_util.dumps(response))

    def check_xsrf_cookie(self):
        pass


def SendShippedMail(email,name,id_orden):
    

    order = Order()
    init_by_id = order.InitById(id_orden)

    if "success" in init_by_id:
        
        detail = OrderDetail()

        lista = detail.ListByOrderId(id_orden)

        if len(lista) > 0:

            detalle_orden = ""

            for l in lista:

                producto = Product()
                response = producto.InitById(l["product_id"])

                

                detalle_orden += """\
                    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                        <td style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid; border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{quantity}</td>
                        <td style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid; border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6; border-top:1px solid #d6d6d6;">{name}</td>
                        <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{color}</td>
                        <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{size}</td>
                        <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">$ {price}</td>
                        <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">$ {subtotal}</td>
                      </tr>
                """.format(name=l["name"].encode("utf-8"),size=l["size"].encode("utf-8"),quantity=l["quantity"],color=l["color"],price=self.money_format(l["sell_price"]).encode("utf-8"),subtotal=self.money_format(l["subtotal"]).encode("utf-8"))

            contact = Contact()
            facturacion_response = contact.InitById(order.billing_id)

            if "success" in facturacion_response:
                facturacion = facturacion_response["success"]
            else:
                print facturacion_response["success"]


            despacho_response = contact.InitById(order.shipping_id)

            if "success" in despacho_response:
                despacho = despacho_response["success"]
            else:
                print despacho_response["success"]

            datos_facturacion = """\
            <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;"><tbody>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th colspan=2 style="line-height: 2.5;height: 30px; border: 1px;border-color: #d6d6d6; border-style: solid; text-align: center;">Datos de Facturaci&oacute;n </th>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">N&deg; Orden </th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{order_id}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Nombre </th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{name}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Direcci&oacute;n</th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{address} - {town} - {city} - {country}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Teléfono</th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{telephone}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Correo</th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{email}</td>
              </tr>
            </tbody></table>
            """.format(order_id=order.id,name=facturacion["name"],address=facturacion["address"],town="",city=facturacion["city"],country="",telephone=facturacion["telephone"],email=facturacion["email"])

            datos_despacho = """\
            <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:20px;"><tbody>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th colspan=2 style="line-height: 2.5;height: 30px; border: 1px;border-color: #d6d6d6; border-style: solid; text-align: center;">Datos de Despacho</th>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">N&deg; Orden </th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{order_id}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Nombre </th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{name}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Direcci&oacute;n</th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{address} - {town} - {city} - {country}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Teléfono</th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{telephone}</td>
              </tr>
              <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Correo</th>
                <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{email}</td>
              </tr>
            </tbody></table>
            """.format(order_id=order.id,name=despacho["name"],address=despacho["address"],town="",city=despacho["city"],country="",telephone=despacho["telephone"],email=despacho["email"])

            html = """\
            <html xmlns=""><head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="initial-scale=1.0"> 
            <meta name="format-detection" content="telephone=no">
            <link href="http://fonts.googleapis.com/css?family=Roboto:300,100,400" rel="stylesheet" type="text/css">
            
            <body style="font-size:12px; font-family:Roboto,Open Sans,Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; background-color:#ffffff; ">

              <table width="100%" id="mainStructure" border="0" cellspacing="0" cellpadding="0" style="background-color:#ffffff;">  
               <!--START TOP NAVIGATION ​LAYOUT-->
               <tr>
                <td valign="top">
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0">


                    <!-- START CONTAINER NAVIGATION -->
                    <tbody><tr>
                      <td align="center" valign="top">

                        <!-- start top navigation container -->
                        <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container">

                          <tbody><tr>
                            <td valign="top">


                              <!-- start top navigaton -->
                              <table width="560" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width">

                                <!-- start space -->
                                <tbody><tr>
                                  <td valign="top" height="20">
                                  </td>
                                </tr>
                                <!-- end space -->

                                <tr>
                                  <td valign="middle">

                                    <table align="center" border="0" cellspacing="0" cellpadding="0" class="container2">

                                      <tbody><tr>
                                        <td align="center" valign="top">
                                         <a href="#"><img src="http://giani.ondev.today/static/images/giani-logo-2-gris-260x119.png" width="250" style="max-width:250px;" alt="Logo" border="0" hspace="0" vspace="0"></a>
                                       </td>

                                     </tr>


                                     <!-- start space -->
                                     <tr>
                                      <td valign="top" class="increase-Height-20">

                                      </td>
                                    </tr>
                                    <!-- end space -->

                                  </tbody></table>

                                  <!--start content nav -->
                                  <!--end content nav -->

                                </td>
                              </tr>

                              <!-- start space -->
                              <tr>
                                <td valign="top" height="20">
                                </td>
                              </tr>
                              <!-- end space -->

                            </tbody></table>
                            <!-- end top navigaton -->
                          </td>
                        </tr>
                      </tbody></table>
                      <!-- end top navigation container -->

                    </td>
                  </tr>


                  <!-- END CONTAINER NAVIGATION -->

                </tbody></table>
              </td>
            </tr>
            <!--END TOP NAVIGATION ​LAYOUT-->
            <!-- START LAYOUT-1/1 --> 

            <tr>
             <td align="center" valign="top" class="fix-box">

               <!-- start  container width 600px --> 
               <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; ">


                 <tbody><tr>
                   <td valign="top">

                     <!-- start container width 560px --> 
                     <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:10px;">


                       <!-- start text content --> 
                       <tbody><tr>
                         <td valign="top">
                           <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
                             <tbody><tr>
                               <td valign="top" width="auto" align="center">
                                 <!-- start button -->                         
                                 <table border="0" align="center" cellpadding="0" cellspacing="0">
                                   <tbody><tr>
                                     <td width="auto" align="center" valign="middle" height="28" style=" background-color:#ffffff; border:1px solid #ececed; background-clip: padding-box; font-size:18px; font-family:Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; text-align:center;  color:#a3a2a2; font-weight: 300; padding-left:18px; padding-right:18px; ">

                                       <span style="color: #a3a2a2; font-weight: 300;">
                                         <a href="#" style="text-decoration: none; color: #a3a2a2; font-weight: 300;">
                                           HOLA <span style="color: #FEBEBD; font-weight: 300;">{name}</span>
                                         </a>
                                       </span>
                                     </td>
                                   </tr>
                                 </tbody></table>
                                 <!-- end button -->   
                               </td>
                             </tr>



                           </tbody></table>
                         </td>
                       </tr>
                       <!-- end text content --> 


                     </tbody></table>
                     <!-- end  container width 560px --> 
                   </td>
                 </tr>
               </tbody></table>
               <!-- end  container width 600px --> 
             </td>
            </tr>

            <!-- END LAYOUT-1/1 --> 


            <!-- START LAYOUT-1/2 --> 

            <tr>
             <td align="center" valign="top" class="fix-box">

               <!-- start  container width 600px --> 
               <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; ">


                 <tbody><tr>
                   <td valign="top">

                     <!-- start container width 560px --> 
                     <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;">


                       <!-- start text content --> 
                       <tbody><tr>
                         <td valign="top">
                           <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">


                             <!-- start text content --> 
                             <tbody><tr>
                               <td valign="top">
                                 <table border="0" cellspacing="0" cellpadding="0" align="center">


                                   <!--start space height --> 
                                   <tbody><tr>
                                     <td height="15"></td>
                                   </tr>
                                   <!--end space height --> 

                                   <tr>
                                     <td style="font-size: 13px; line-height: 22px; font-family:Roboto,Open Sans,Arial,Tahoma, Helvetica, sans-serif; color:#a3a2a2; font-weight:300; text-align:center; ">


                                       Tu producto ha sido enviado.


                                     </td>
                                   </tr>

                                   <!--start space height --> 
                                   <tr>
                                     <td height="15"></td>
                                   </tr>
                                   <!--end space height --> 



                                 </tbody></table>
                               </td>
                             </tr>
                             <!-- end text content -->

                             <tr>
                               <td valign="top" width="auto" align="center">

                               </td>

                             </tr>

                           </tbody></table>
                         </td>
                       </tr>
                       <!-- end text content --> 

                       <!--start space height --> 
                       <tr>
                         <td height="20"></td>
                       </tr>
                       <!--end space height --> 


                     </tbody></table>
                     <!-- end  container width 560px --> 
                   </td>
                 </tr>
               </tbody></table>
               <!-- end  container width 600px --> 
             </td>
            </tr>

            <!-- END LAYOUT-1/2 --> 
            <!-- START LAYOUT-9 --> 

            <tr>
             <td align="center" valign="top" class="fix-box">

               <!-- start  container width 600px --> 
               <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; border-bottom:1px solid #c7c7c7; border-top:1px solid #c7c7c7;">

                <!--start space height --> 
                <tbody><tr>
                 <td height="20" valign="top"></td>
               </tr>
               <!--end space height --> 

               <tr>
                 <td valign="top">

                   <!-- start container width 560px --> 
                   <table width="560" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;">




                     <!-- start heading -->               
                     <tbody><tr>     
                       <td valign="top">
                         <table width="100%" border="0" cellspacing="0" cellpadding="0" align="left">
                           <tbody><tr>


                             <td align="left" style="font-size: 18px; line-height: 22px; font-family:Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; color:#555555; font-weight:300; text-align:left;">
                               <span style="color: #555555; font-weight:300;">
                                 <a href="#" style="text-decoration: none; color: #555555; font-weight: 300;">Trackea tu producto </a>
                               </span>
                             </td>

                           </tr>
                         </tbody></table>
                       </td>
                     </tr>
                     <!-- end heading -->  

                     <!--start space height --> 
                     <tr>
                       <td height="15"></td>
                     </tr>
                     <!--end space height --> 
                     
                     <!-- start text content -->
                     <tr>
                       <td valign="top">
                         <table border="0" cellspacing="0" cellpadding="0" align="left">


                           <tbody><tr>
                             <td style="font-size: 13px; line-height: 22px; font-family:Roboto,Open Sans,Arial,Tahoma, Helvetica, sans-serif; color:#a3a2a2; font-weight:300; text-align:left; ">

                               usa este código en correos de chile. {tracking_code}

                             </td>
                           </tr>


                         </tbody></table>

                       </td>
                       
                     </tr>

                     <!-- end text content -->

                     <!--start space height --> 
                     <tr>
                       <td height="15"></td>
                     </tr>
                     <!--end space height --> 

                     <!--start space height --> 
                     <tr>
                       <td height="20" valign="top"></td>
                     </tr>
                     <!--end space height --> 

                     

                   </tbody></table>
                   <!-- end  container width 560px --> 
                 </td>
               </tr>
             </tbody></table>
             <!-- end  container width 600px --> 
            </td>
            </tr>

            <!-- END LAYOUT-9 --> 

            <!-- START LAYOUT-1/2 --> 

            <tr>
             <td align="center" valign="top" class="fix-box">

               <!-- start  container width 600px --> 
               <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; padding-bottom:20px; ">


                 <tbody><tr>
                   <td valign="top">

                     <!-- start container width 560px --> 
                     <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;">


                       <!-- start text content --> 
                       <tbody><tr>
                         <td valign="top">
                           <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">


                             <!-- start text content --> 
                             <tbody><tr>
                               <td valign="top">
                                 <table border="0" cellspacing="0" cellpadding="0" align="center">


                                   <!--start space height --> 
                                   <tbody><tr>
                                     <td height="15"></td>
                                   </tr>
                                   <!--end space height --> 

                                   <tr>
                                     <td style="font-size: 13px; line-height: 22px; font-family:Roboto,Open Sans,Arial,Tahoma, Helvetica, sans-serif; color:#a3a2a2; font-weight:300; text-align:center; ">





                                     </td>
                                   </tr>

                                   <!--start space height --> 
                                   <tr>
                                     <td height="15"></td>
                                   </tr>
                                   <!--end space height --> 



                                 </tbody></table>
                               </td>
                             </tr>
                             <!-- end text content -->

                             <tr>
                               <td valign="top" width="auto" align="center">

                               </td>

                             </tr>

                           </tbody></table>
                         </td>
                       </tr>
                       <!-- end text content --> 

                       <!--start space height --> 
                       <tr>
                         <td height="20"></td>
                       </tr>
                       <!--end space height --> 


                     </tbody></table>


                    {datos_facturacion}
                    {datos_despacho}

                    <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:20px;"><tbody>
                      <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                        <th colspan=2 style="line-height: 2.5;height: 30px; border: 1px;border-color: #d6d6d6; border-style: solid; text-align: center;">Datos compra</th>
                      </tr>
                    </tbody></table>
                    <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;"><tbody>
                      <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                        <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6; border-right: 1px solid #d6d6d6;">Cantidad</th>
                        <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Nombre producto</th>
                        <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid; border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Color</th>
                        <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Talla</th>
                        <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Precio</th>
                        <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Subtotal</th>
                      </tr>
                        
                        {detalle_orden}

                    </tbody></table>

                    <table width="540" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:20px;"><tbody>
                      <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                        <th colspan=2 style="line-height: 2.5;height: 30px; border: 1px;border-color: #d6d6d6; border-style: solid; text-align: center;">Resumen</th>
                      </tr>
                      <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                        <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Subtotal </th>
                        <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">$ {order_subtotal}</td>
                      </tr>
                      <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                        <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Costo de Env&iacute;o</th>
                        <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">$ {costo_despacho}</td>
                      </tr>
                      <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
                        <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Total</th>
                        <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">$ {order_total}</td>
                      </tr>
                    </tbody></table>
                    <!-- end  container width 560px --> 
                  </td>
                </tr>
              </tbody></table>
              <!-- end  container width 600px --> 
            </td>
            </tr>

            <!-- END LAYOUT-1/2 --> 

            <!--START FOOTER LAYOUT-->
            <tr>
              <td valign="top">
                <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0">

                  <!-- START CONTAINER  -->
                  <tbody><tr>
                    <td align="center" valign="top">

                      <!-- start footer container -->
                      <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container">

                        <tbody><tr>
                          <td valign="top">


                            <!-- start footer -->
                            <table width="560" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width">

                              <!-- start space -->
                              <tbody><tr>
                                <td valign="top" height="20">
                                </td>
                              </tr>
                              <!-- end space -->

                              <tr>
                                <td valign="middle">

                                  <table align="left" border="0" cellspacing="0" cellpadding="0" class="container2">

                                    <tbody><tr>
                                      <td align="center" valign="top">
                                       <a href="#"><img src="http://giani.ondev.today/static/images/giani-logo-2-gris-260x119.png" width="114" style="max-width:114px;" alt="Logo" border="0" hspace="0" vspace="0"></a>
                                     </td>
                                     
                                   </tr>

                                   <!-- start space -->
                                   <tr>
                                    <td valign="top" class="increase-Height-20">
                                    </td>
                                  </tr>
                                  <!-- end space -->

                                </tbody></table>

                              </td>
                            </tr>

                            <!-- start space -->
                            <tr>
                              <td valign="top" height="20">
                              </td>
                            </tr>
                            <!-- end space -->

                          </tbody></table>
                          <!-- end footer -->
                        </td>
                      </tr>
                    </tbody></table>
                    <!-- end footer container -->

                  </td>
                </tr>
                

                <!-- END CONTAINER  -->
                
              </tbody></table>
            </td>
            </tr>
            <!--END FOOTER ​LAYOUT-->



            <!--  START FOOTER COPY RIGHT -->

            <tr>
              <td align="center" valign="top" style="background-color:#FEBEBD;">
                <table width="600" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color:#FEBEBD;">
                  <tbody><tr>
                    <td valign="top">
                      <table width="560" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color:#FEBEBD;">

                        <!--start space height -->                      
                        <tbody><tr>
                          <td height="10"></td>
                        </tr>
                        <!--end space height --> 

                        <tr>
                          <!-- start COPY RIGHT content -->  
                          <td valign="top" style="font-size: 13px; line-height: 22px; font-family:Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; color:#ffffff; font-weight:300; text-align:center; ">
                           GIANI DA FIRENZE 2014 ®
                         </td>
                         <!-- end COPY RIGHT content --> 
                       </tr>

                       <!--start space height -->                      
                       <tr>
                        <td height="10"></td>
                      </tr>
                      <!--end space height --> 


                    </tbody></table>
                  </td>
                </tr>
              </tbody></table>
            </td>
            </tr>
            <!--  END FOOTER COPY RIGHT -->
            </table>

            </table>
            </body></html>
            """.format(name=despacho["name"],
                order_id=order.id,
                datos_facturacion=datos_facturacion,
                datos_despacho=datos_despacho,
                detalle_orden=detalle_orden,
                order_total=self.money_format(order.total+order.shipping),
                order_subtotal=self.money_format(order.subtotal),
                order_tax=self.money_format(order.tax),
                url_local=url_local,
                costo_despacho=self.money_format(order.shipping),
                tracking_code=tracking_code)

            # email_confirmacion = "yichun212@gmail.com"

            sg = sendgrid.SendGridClient('nailuj41', 'Equipo_1234')
            message = sendgrid.Mail()
            message.set_from("{nombre} <{mail}>".format(nombre="Giani Da Firenze",mail=email_giani))
            message.add_to(self.current_user["email"])
            message.set_subject("Giani Da Firenze - Compra Nº {}".format(order.id))
            message.set_html(html)
            status, msg = sg.send(message)

            if status != 200:
                print "Error al enviar correo de confirmación, {}".format(msg)

        else:

            print "Detalle vacío" 