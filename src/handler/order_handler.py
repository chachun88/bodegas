#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from ..globals import *

from basehandler import BaseHandler
from ..model10.order import Order
from ..model10.product import Product
from ..model10.shipping import Shipping
from ..model10.customer import Customer
from ..model10.cellar import Cellar
from emails import TrackingCustomer

from datetime import datetime
import sendgrid
from bson import json_util

import pytz

ACCIONES_ELIMINAR = 1
ACCIONES_CONFIRMAR = 2
ACCIONES_PARA_DESPACHO = 3
ACCIONES_DESPACHADO = 4
ACCIONES_CANCELADO = 5


class OrderHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.PEDIDOS_LISTA)

        pjax = bool(self.get_argument("_pjax", False))

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        self.render("order{}/home.html".format(pjax_str),
                    side_menu=self.side_menu,
                    dn=self.get_argument("dn", ""))


class AddOrderHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        order = Order()
        self.render("order/save.html", dn="", mode="add", order=order)

    @tornado.web.authenticated
    def post(self):

        # instantiate order
        order = Order()

        order.id = self.get_argument("id", "")
        order.date = datetime.now(
            pytz.timezone('Chile/Continental').isoformat())
        order.salesman = self.get_argument("salesman", "")
        order.customer = self.get_argument("customer", "")
        order.subtotal = self.get_argument("subtotal", "")
        order.discount = self.get_argument("discount", "")
        order.tax = self.get_argument("tax", "")
        order.total = self.get_argument("total", "")
        order.address = self.get_argument("address", "")
        order.town = self.get_argument("town", "")
        order.city = self.get_argument("city", "")
        order.country = self.get_argument("country", "")
        order.type = self.get_argument("type", "")
        order.source = self.get_argument("source", "")
        order.items_quantity = self.get_argument("items_quantity", "")
        order.product_quantity = self.get_argument("product_quantity", "")
        order.state = self.get_argument("state", "")

        # saving the current order
        oid = order.Save()

        self.write(oid)


class OrderActionsHandler(BaseHandler):

    # @tornado.web.authenticated
    def post(self):

        order = Order()

        resultado = []

        valores = self.get_argument("values", "").split(",")
        accion = self.get_argument("action", "")

        if accion == "":
            self.write("Debe seleccionar una acción")
            return

        accion = int(accion)

        if len(valores) == 0:
            self.write("Debe seleccionar al menos un pedido")
            return

        for v in valores:

            if accion == ACCIONES_ELIMINAR:

                response = order.DeleteOrder(v)

                resultado.append(response)

            elif accion == ACCIONES_CONFIRMAR:

                _order = Order()
                res_order = _order.InitWithId(v)

                if "success" in res_order:
                    if _order.state == Order.ESTADO_PENDIENTE and _order.payment_type == 1:
                        order.ChangeStateOrders(v, Order.ESTADO_CONFIRMADO)
                        SendConfirmedMail(
                            _order.customer_email, _order.customer, v)
                    elif _order.state == Order.ESTADO_PENDIENTE and _order.payment_type == 3:
                        order.ChangeStateOrders(v, Order.ESTADO_CONFIRMADO)
                    else:
                        resultado.append(
                            {"error": "el pedido {} no puede ser confirmado".format(_order.id)})
                else:
                    resultado.append(res_order)

            elif accion == ACCIONES_PARA_DESPACHO:

                _order = Order()
                res_order = _order.InitWithId(v)

                if "success" in res_order:
                    if _order.state == Order.ESTADO_CONFIRMADO:
                        res = order.ChangeStateOrders(
                            v, Order.ESTADO_PARA_DESPACHO)
                        resultado.append(res)
                    else:
                        resultado.append(
                            {"error": "el pedido {} no puede cambiar a estado listo para despacho".format(_order.id)})
                else:
                    resultado.append(res_order)

            elif accion == ACCIONES_CANCELADO:

                cellar_id = None
                web_cellar = None

                cellar = Cellar()
                res_reservation_cellar = cellar.GetReservationCellar()

                errores = []

                if "success" in res_reservation_cellar:
                    cellar_id = res_reservation_cellar["success"]
                else:
                    return self.ShowError(res_reservation_cellar["error"])

                res_web_cellar = cellar.GetWebCellar()

                if "success" in res_web_cellar:
                    web_cellar = res_web_cellar["success"]
                else:
                    errores.append("bodega web no encontrado")

                _order = Order()
                res_order = _order.InitWithId(v)

                if "success" in res_order:

                    if _order.state == Order.ESTADO_CONFIRMADO or _order.state == Order.ESTADO_PENDIENTE or _order.ESTADO_PARA_DESPACHO:

                        res_cancel = order.cancel(v, cellar_id, web_cellar)

                        if "success" in res_cancel:
                            response = order.ChangeStateOrders(
                                v, Order.ESTADO_CANCELADO)
                            resultado.append(response)
                        else:
                            resultado.append(res_cancel)
                    else:
                        resultado.append(
                            {"error": "el pedido {} no puede ser cancelado".format(_order.id)})
                else:
                    resultado.append(res_order)

            ''' replaced by shipping_handler.SaveTrackingCodeHandler'''
        # print '--------------------'
        # print resultado
        # print '--------------------'
        self.write(json_util.dumps(resultado))
        # return

        # elif accion == ACCIONES_DESPACHADO:

        #     shipping = Shipping()

        #     errores = []

        #     arr_tracking_code = self.get_arguments("tracking_code")

        #     arr_provider_id = self.get_arguments("provider_id")

        #     arr_order_id = self.get_arguments("order_id")

        #     for x in range(0, len(arr_order_id)):

        #         order_id = arr_order_id[x]
        #         tracking_code = arr_tracking_code[x]
        #         provider_id = arr_provider_id[x]

        #         provider_name = ""

        #         res = shipping.SaveTrackingCode(order_id,tracking_code,provider_id, reserve_cellar_id)

        #         if "error" in res:
        #             errores.append(res["error"])
        #         else:
        #             if int(provider_id) == 1:
        #                 provider_name = "Chilexpress"
        #             elif int(provider_id) == 2:
        #                 provider_name = "Correos de Chile"

        #             customer = Customer()
        #             response = customer.InitById(res["success"])

        #             if response == "ok":
        #                 TrackingCustomer(customer.email,customer.name,tracking_code,provider_name,order_id)

        #     if len(errores) > 0:
        #         self.write(json_util.dumps({"state":1,"obj":errores}))
        #     else:
        #         self.write(json_util.dumps({"state":0}))

    def check_xsrf_cookie(self):
        pass


class OrderAjaxListHandler(BaseHandler):

    def get(self):
        start = int(self.get_argument("start", 0))
        items = int(self.get_argument("length", 20))
        if items == -1:
          items = 0
        term = self.get_argument("search[value]", "")
        query = ""

        if term != "":
            if term.lower() == 'confirmado':
                query = '''where o.state = 2'''
            elif term.lower() == 'rechazado':
                query = '''where o.state = 1 and o.payment_type = 2'''
            elif term.lower() == 'por confirmar':
                query = '''where (o.state = 1 and o.payment_type = 1) or (o.state = 1 and o.payment_type = 3)'''
            elif term.lower() == 'para despachar':
                query = '''where o.state = 3'''
            elif term.lower() == 'despachado':
                query = '''where o.state = 4'''
            elif term.lower() == 'cancelado':
                query = '''where o.state = 5'''
            elif term.lower() == 'mayorista' or term.lower() == 'cliente mayorista':
                query = '''where ut.id = 4'''
            elif term.lower() == 'transferencia':
                query = '''where o.payment_type = 1'''
            elif term.lower() == 'webpay':
                query = '''where o.payment_type = 2'''
            else:
              try:
                term = int(term)
                query = """where o.id = %(term)s"""
              except:
                query = """where unaccent(lower(coalesce(c.name, '') || ' ' || coalesce(c.lastname, ''))) like %(term)s"""
                term = "%{}%".format(term)

        columns = [
            ""
            "order_id",
            "o.date",
            "customer",
            "tipo_cliente",
            "source",
            "total",
            "o.state",
            "payment_type"
        ]

        column = int(self.get_argument("order[0][column]"))
        direction = self.get_argument("order[0][dir]")

        try:
          page = int(start / items) + 1
        except:
          page = 0

        total_items = 0

        if column > 0:
            column -= 1
        else:
            direction = 'desc'

        order = Order()
        pedidos = order.List(
            page, items, query, columns[column], direction, term)
        res_total_items = order.getTotalItems(query, term)

        if "success" in res_total_items:
            total_items = res_total_items["success"]

        result = {
            "recordsTotal": total_items,
            "recordsFiltered": total_items,
            "data": pedidos
        }

        self.write(json_util.dumps(result))

        # self.render("order/home.html",
        #             side_menu=self.side_menu,
        #             pedidos=pedidos,
        #             dn=self.get_argument("dn", ""),
        #             page=page,
        #             total_pages=total_pages)


def SendConfirmedMail(email, name, id_orden):

    html = """\
    <html xmlns=""><head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="initial-scale=1.0"> 
        <meta name="format-detection" content="telephone=no">
        <link href="http://fonts.googleapis.com/css?family=Roboto:300,100,400" rel="stylesheet" type="text/css">




        </head>

        <body style="font-size:12px; font-family:Roboto,Open Sans,Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; background-color:#ffffff; ">

        <!--start 100%wrapper (white background) -->
        <table width="100%" id="mainStructure" border="0" cellspacing="0" cellpadding="0" style="background-color:#ffffff;">  


           <!--START VIEW ONLINE AND ICON SOCAIL -->
          <tbody>
           <!--END VIEW ONLINE AND ICON SOCAIL-->






            <!--START TOP NAVIGATION ​LAYOUT-->
          <tr>
            <td valign="top">
              <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0">


              <!-- START CONTAINER NAVIGATION -->
              <tbody><tr>
                <td align="center" valign="top">
                  
                  <!-- start top navigation container -->
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container">
                    
                    <tbody><tr>
                      <td valign="top">
                          

                        <!-- start top navigaton -->
                        <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width">

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
                                   <a href="#"><img src="{url_local}/static/images/giani-logo-2-gris-260x119.png" width="250" style="max-width:250px;" alt="Logo" border="0" hspace="0" vspace="0"></a>
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



        <!-- START HEIGHT SPACE 20PX LAYOUT-1 -->
         <tr>
           <td valign="top" align="center" class="fix-box">
             <table width="100%" height="20" align="center" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff;" class="full-width">
               <tbody><tr>
                 <td valign="top" height="20">  
                   </td>
               </tr>
             </tbody></table>
           </td>
         </tr>
         <!-- END HEIGHT SPACE 20PX LAYOUT-1-->


         <!-- START LAYOUT-1/1 --> 

         <tr>
           <td align="center" valign="top" class="fix-box">

             <!-- start  container width 600px --> 
             <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; ">


               <tbody><tr>
                 <td valign="top">

                   <!-- start container width 560px --> 
                   <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin: 0px auto;">


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
             <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; ">


               <tbody><tr>
                 <td valign="top">

                   <!-- start container width 560px --> 
                   <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin: 0px auto;">


                     <!-- start text content --> 
                     <tbody><tr>
                       <td valign="top">
                         <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" margin: style="0px auto;">
                           

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
                                   <td style="font-size: 13px; line-height: 22px; font-family:Roboto,Open Sans,Arial,Tahoma, Helvetica, sans-serif; color:#a3a2a2; font-weight:300; text-align:center;">
                                       Hemos confirmado tu pago, el pedido n&uacute;mero {order_id} se empezar&aacute; a procesar
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
         <!--START FOOTER LAYOUT-->
          <tr>
            <td valign="top">
              <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0">


              <!-- START CONTAINER  -->
              <tbody><tr>
                <td align="center" valign="top">
                  
                  <!-- start footer container -->
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container">
                    
                    <tbody><tr>
                      <td valign="top">
                          

                        <!-- start footer -->
                        <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width">

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
                                   <a href="#"><img src="{url_local}/static/images/giani-logo-2-gris-260x119.png" width="114" style="max-width:114px;" alt="Logo" border="0" hspace="0" vspace="0"></a>
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
            <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color:#FEBEBD;">
              <tbody><tr>
                <td valign="top">
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color:#FEBEBD;">

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


        </tbody></table>
        <!-- end 100%wrapper (white background) -->



        </body></html>
                """.format(name=name, order_id=id_orden, url_local=url_local)

    sg = sendgrid.SendGridClient(usuario_sendgrid, pass_sendgrid)
    message = sendgrid.Mail()
    message.set_from(
        "{nombre} <{mail}>".format(nombre="Giani Da Firenze", mail=from_giani))
    message.add_to(email)
    message.set_subject(
        "Giani Da Firenze - El pago de la orden Nº {} ha sido confirmado".format(id_orden))
    message.set_html(html)
    status, msg = sg.send(message)

    if status != 200:
        print "Error al enviar correo de confirmación, {}".format(msg)
