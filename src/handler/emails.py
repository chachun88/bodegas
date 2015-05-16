#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.web
from basehandler import BaseHandler
from bson import json_util
import sendgrid

from ..model10.order import Order
from ..model10.order_detail import OrderDetail
from ..model10.contact import Contact
from ..globals import email_giani, usuario_sendgrid, pass_sendgrid

def TrackingCustomer(email,name,tracking_code,provider_name,order_id):


    order = Order()
    order.InitWithId(str(order_id))

    contact = Contact()
    contact.InitById(order.billing_id)

    order_detail = OrderDetail()
    listbyorderid = order_detail.ListByOrderId(order_id)

    datos_facturacion = """\
    <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;"><tbody>
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
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{address} - {town} - {city}</td>
    </tr>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Teléfono</th>
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{telephone}</td>
    </tr>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Correo</th>
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{email}</td>
    </tr>
    </tbody></table>""".format( order_id=order_id,
                                name=contact.name,
                                address=contact.address.encode("utf-8"),
                                town=contact.town.encode("utf-8"),
                                city=contact.city,
                                telephone=contact.telephone,
                                email=contact.email.encode("utf-8"))
    

    contact.InitById(order.shipping_id)

    datos_despacho = """\
    <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:20px;"><tbody>
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
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{address} - {town} - {city}</td>
    </tr>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Teléfono</th>
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{telephone}</td>
    </tr>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Correo</th>
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{email}</td>
    </tr>
    </tbody></table>""".format( order_id=order_id,
                                name=contact.name.encode("utf-8"),
                                address=contact.address.encode("utf-8"),
                                town=contact.town.encode("utf-8"),
                                city=contact.city,
                                telephone=contact.telephone,
                                email=contact.email.encode("utf-8"))


    items_compra = ""

    if "success" in listbyorderid:

        details = listbyorderid["success"]

        for d in details:
            items_compra += """\
            <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
              <td style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid; border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{quantity}</td>
              <td style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid; border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{name}</td>
              <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{color}</td>
              <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{size}</td>
              <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{price}</td>
              <td style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{subtotal}</td>
            </tr>""".format(quantity=d["quantity"],name=d["name"].encode("utf-8"),size=d["size"],price=BaseHandler.money_format(d["price"]),subtotal=BaseHandler.money_format(d["subtotal"]),color=d["color"].encode("utf-8"))

    datos_compra = """\
    <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:20px;"><tbody>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th colspan=2 style="line-height: 2.5;height: 30px; border: 1px;border-color: #d6d6d6; border-style: solid; text-align: center;">Datos compra</th>
    </tr>
    </tbody></table>
    <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;"><tbody>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Cantidad</th>
      <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Nombre producto</th>
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid; border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Color</th>
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Talla</th>
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Precio</th>
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Subtotal</th>
    </tr>
    {items_compra}
    </tbody></table>""".format(items_compra=items_compra)

    resumen = """\
    <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:20px;"><tbody>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th colspan=2 style="line-height: 2.5;height: 30px; border: 1px;border-color: #d6d6d6; border-style: solid; text-align: center;">Resumen</th>
    </tr>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Subtotal </th>
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{order_subtotal}</td>
    </tr>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Costo de Env&iacute;o</th>
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{costo_despacho}</td>
    </tr>
    <tr style="font-family: Arial;background-color: #FFFFFF;text-align: center; font-size:12px;">
      <th style="line-height: 2.5;margin-right: -1px;height: 30px;border-left: 1px;border-left-color: #d6d6d6; border-left-style: solid;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">Total</th>
      <td style="line-height: 2.5;margin-left: -1px;height: 30px;border-right: 1px;border-right-color: #d6d6d6; border-right-style: solid;border-bottom: 1px; border-bottom-style: solid;border-bottom-color: #d6d6d6;">{order_total}</td>
    </tr>
    </tbody></table>
    """.format(order_subtotal=BaseHandler.money_format(order.subtotal),costo_despacho=BaseHandler.money_format(order.shipping),order_total=BaseHandler.money_format(order.subtotal+order.shipping))
  

    html = """\
    <html xmlns="">
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <meta name="viewport" content="initial-scale=1.0">
      <meta name="format-detection" content="telephone=no">
      <link href="http://fonts.googleapis.com/css?family=Roboto:300,100,400" rel="stylesheet" type="text/css">
    </head>
    <body style="font-size:12px; font-family:Roboto,Open Sans,Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; background-color:#ffffff; ">
      <table width="100%" id="mainStructure" border="0" cellspacing="0" cellpadding="0" style="background-color:#fffff;">
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
            <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; ">
              <tbody><tr>
                <td valign="top">
                  <!-- start container width 560px -->
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;margin-top:10px;">
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
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;">
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
            <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; border-bottom:1px solid #c7c7c7; border-top:1px solid #c7c7c7;">
              <!--start space height -->
              <tbody><tr>
                <td height="20" valign="top"></td>
              </tr>
              <!--end space height -->
              <tr>
                <td valign="top">
                  <!-- start container width 560px -->
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;">
                    <!-- start heading -->
                    <tbody><tr>
                      <td valign="top">
                        <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
                          <tbody><tr>
                            <td align="center" style="font-size: 18px; line-height: 22px; font-family:Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; color:#555555; font-weight:300; text-align:left;">
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
                        <table border="0" cellspacing="0" cellpadding="0" align="center">
                          <tbody><tr>
                            <td style="font-size: 13px; line-height: 22px; font-family:Roboto,Open Sans,Arial,Tahoma, Helvetica, sans-serif; color:#a3a2a2; font-weight:300; text-align:left; ">
                              Usa este c&oacute;digo en {provider_name}. {tracking_code}
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
            <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="container" style="background-color: #ffffff; padding-bottom:20px; ">
              <tbody><tr>
                <td valign="top">
                  <!-- start container width 560px -->
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width" bgcolor="#ffffff" style="background-color:#ffffff;">
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
                  {datos_compra}
                  {resumen}

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
      </table>
    </table>
    </body></html>
    """.format(name=name,provider_name=provider_name,tracking_code=tracking_code,datos_facturacion=datos_facturacion,datos_compra=datos_compra,datos_despacho=datos_despacho,resumen=resumen)


  
                  

    sg = sendgrid.SendGridClient(usuario_sendgrid, pass_sendgrid)

    message = sendgrid.Mail()
    message.set_from("{nombre} <{mail}>".format(nombre="Giani Da Firenze", mail=email_giani))
    message.add_to(email)
    message.set_subject("Giani Da Firenze - El pedido Nº {order_id} ha sido enviado".format(order_id=order_id))
    message.set_html(html)

    status, msg = sg.send(message)

    json_obj = json_util.loads(msg)

    if json_obj["message"] == "success":
        print "se envio exitosamente"
    else:
        print json_obj["errors"]
