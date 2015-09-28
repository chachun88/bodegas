#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 25/02/2013

@author: Yi Chun
'''
from basehandler import *
from email.mime.multipart import MIMEMultipart
from tornado.options import options
from random import randrange
import hashlib
import sendgrid
import json

from src.globals import *


class EnviarClaveHandler(BaseHandler):

    def post(self):
        email = self.get_argument("email")
        if(len(email) > 0):
            usuario = self.db.user.find_one(
                {"mail": email, "tipo": "registrado"})
            if usuario:
                clave = str(randrange(100))
                clave = hashlib.md5(clave).hexdigest()[:6]
                self.db.user.update(
                    {"_id": usuario["_id"]}, {"$set": {"password": clave}})

                # if lptranslate("lang") == "es":
                Email(usuario["mail"], str(usuario["_id"]), clave)
                # elif lptranslate("lang") == "en":
                #     EmailEn(usuario["mail"], str(usuario["_id"]), clave)

                self.redirect("/")
            else:
                self.write("Usuario no se encuentra registrado")
        else:
            self.write("Ingrese email por favor")


def RegistrationEmail(username,email):

    html = """\
          <html xmlns="">
          <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <meta name="viewport" content="initial-scale=1.0">
            <meta name="format-detection" content="telephone=no">
            <link href="http://fonts.googleapis.com/css?family=Roboto:300,100,400" rel="stylesheet" type="text/css">
          </head>
        <body style="font-size:12px; font-family:Roboto,Open Sans,Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; background-color:#ffffff; ">
          <!--start 100% wrapper (white background) -->
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
                                    
                                    <table align="center" border="0" cellspacing="0" cellpadding="0" class="container2" style="margin: 0px auto;">
                                      
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
                              <table width="100%" border="0" cellspacing="0" cellpadding="0" align="center" style="margin: 0px auto;">
                                
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
                                          
                                          Bienvenid@ a la comunidad GIANI DA FIRENZE disfruta de nuestras novedades y modelos
                                          
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
                                    <!-- start button -->
                                    <table border="0" align="center" cellpadding="0" cellspacing="0">
                                      <tbody><tr>
                                        <td width="auto" align="center" valign="middle" height="32" style=" background-color:#FEBEBD;  border-radius:5px; background-clip: padding-box;font-size:13px; font-family:Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; text-align:center;  color:#ffffff; font-weight: 300; padding-left:18px; padding-right:18px; ">
                                          <span style="color: #ffffff; font-weight: 300;">
                                          <a href="{url_local}" style="text-decoration: none; color: #FFFFFF; font-weight: 300;">
                                            Visita nuestro store
                                          </a>
                                          </span>
                                        </td>
                                        <!-- start space width -->
                                        <td valign="top">
                                          <table width="20" border="0" align="center" cellpadding="0" cellspacing="0">
                                            <tbody><tr>
                                              <td valign="top">
                                                &nbsp;
                                              </td>
                                            </tr>
                                          </tbody></table>
                                        </td>
                                        <!--end space width -->
                                      </tr>
                                    </tbody></table>
                                    <!-- end button -->
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
              <!--START IMAGE HEADER LAYOUT-->
              <tr>
                <td align="center" valign="top" class="fix-box">
                  <!-- start HEADER LAYOUT-container width 600px -->
                  <table width="100%" align="center" border="0" cellspacing="0" cellpadding="0" class="full-width">
                    <tbody><tr>
                      <td valign="top" class="image-100-percent">
                        
                        <img src="http://giani.ondev.today/static/images/baner.png" width="100%" alt="header-image" style="display:block !important;">
                        
                      </td>
                    </tr>
                  </tbody></table>
                  <!-- end HEADER LAYOUT-container width 600px -->
                </td>
              </tr>
              <!--END IMAGE HEADER LAYOUT-->
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
            </tbody></table>
            <!-- end 100% wrapper (white background) -->
          </body></html>
          """.format(name=username.encode("utf-8"),url_local=url_local)
    sg = sendgrid.SendGridClient(sendgrid_user, sendgrid_pass)

    message = sendgrid.Mail()
    message.set_from("{nombre} <{mail}>".format(
        nombre="Giani Da Firenze", mail=email_giani))
    message.add_to(email)
    message.set_subject("Bienvenida a Giani Da Firenze")
    message.set_html(html)

    status, msg = sg.send(message)

    json_obj = json.loads(msg)

    if json_obj["message"] == "success":
        print "se envio exitosamente"
    else:
        print json_obj["errors"]


def Email(to, userid, clave, name=""):

    fromaddr = options.email
    toaddrs = to
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Restablecimiento de clave de la cuenta Giani da Firenze"
    msg['From'] = "Giani da Firenze " + "<" + fromaddr + ">"
    msg['To'] = toaddrs

    # Credentials (if needed)
    username = options.user
    password = options.password

    html = """\
    <html xmlns=""><head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="initial-scale=1.0"> 
<meta name="format-detection" content="telephone=no">
<link href="http://fonts.googleapis.com/css?family=Roboto:300,100,400" rel="stylesheet" type="text/css">




</head>

<body style="font-size:12px; font-family:Roboto,Open Sans,Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; background-color:#ffffff; ">

<!--start 100% wrapper (white background) -->
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
                           <td style="font-size: 13px; line-height: 22px; font-family:Roboto,Open Sans,Arial,Tahoma, Helvetica, sans-serif; color:#a3a2a2; font-weight:300; text-align:center; ">

                             
                               Cambiar tu contraseña es simple. Por favor usa el siguiente link
                             

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
                       <!-- start button -->                         
                       <table border="0" align="center" cellpadding="0" cellspacing="0">
                         <tbody><tr>
                           <td width="auto" align="center" valign="middle" height="32" style=" background-color:#FEBEBD;  border-radius:5px; background-clip: padding-box;font-size:13px; font-family:Roboto,Open Sans, Arial,Tahoma, Helvetica, sans-serif; text-align:center;  color:#ffffff; font-weight: 300; padding-left:18px; padding-right:18px; ">

                             <span style="color: #ffffff; font-weight: 300;">
                               <a href="{url_local}/auth/nuevaclave/{userid}?clave={clave}" style="text-decoration: none; color: #FFFFFF; font-weight: 300;">
                                link
                               </a>
                             </span>
                           </td>

                           <!-- start space width -->
                            <td valign="top">
                              <table width="20" border="0" align="center" cellpadding="0" cellspacing="0">
                                <tbody><tr>
                                  <td valign="top">
                                    &nbsp;
                                  </td>
                                </tr>
                              </tbody></table>
                            </td>
                            <!--end space width -->

                         </tr>
                       </tbody></table>
                       <!-- end button -->   
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


</tbody></table>
<!-- end 100% wrapper (white background) -->



</body></html>
        """.format(name=name, url_local=url_local, userid=userid, clave=clave)

    text = "Hola, tu nueva clave es: " + clave + \
        "\n por favor ingresa aqui para reestablecer tu clave : " + \
        url_local + "/auth/nuevaclave/" + userid

    # Record the MIME types of both parts - text/plain and text/html.
    # part1 = MIMEText(text, 'plain')
    # part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    # msg.attach(part1)
    # msg.attach(part2)

    # The actual mail send
    # server = smtplib.SMTP('smtp.gmail.com:587')
    # server.starttls()
    # server.login(username, password)
    # server.sendmail(fromaddr, toaddrs, msg.as_string())
    # server.quit()

    sg = sendgrid.SendGridClient(sendgrid_user, sendgrid_pass)

    message = sendgrid.Mail()
    message.set_from("{nombre} <{mail}>".format(
        nombre="Giani Da Firenze", mail=email_giani))
    message.add_to(to)
    message.set_subject("Reestablece tu contraseña")
    message.set_html(html)

    status, msg = sg.send(message)

    json_obj = json.loads(msg)

    if json_obj["message"] == "success":
        print "se envio exitosamente"
    else:
        print json_obj["errors"]
