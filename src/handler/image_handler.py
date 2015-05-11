#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from PIL import Image
import StringIO

import time
import os
import glob
import os.path

from ..globals import *

from basehandler import BaseHandler

DEFAULT_IMAGE = "static/default_image.jpg"

def getIamgeBuffer(handler, image_name):

    ### case 1 user ask for full image
    wwidth = int(handler.get_argument("mw", -1))

    if wwidth == -1:
        ### show full image
        try:
            image_path = dir_img + image_name
            f = open(image_path, "rb")
            buff = f.read()
            f.close()

            #print "retorna original"

            return buff
        except Exception, e:
            pass ## continue to default image
    else:
        ## show scaled image
        try: # detect if image exist
            f = open( dir_img + "{}{}".format(wwidth, image_name), "rb")
            buff = f.read()
            f.close()

            return buff
        except Exception, ex:
            #print str(ex)
            try:
                ##image doesnt exist so i create it
                image_path = dir_img + "{}{}".format(wwidth, image_name)

                ## getting variables
                orig = Image.open( dir_img + image_name)
                width = int(orig.size[0])
                height = int(orig.size[1])
                max_width = int(handler.get_argument("mw", "{}".format(width)))

                # resampling image
                im = orig.resize((max_width,height * max_width / width), Image.ANTIALIAS)

                # convert pil image to bytes buffer
                buf= StringIO.StringIO()
                im.save(buf, format= 'PNG')
                im.save( dir_img + "{}{}".format(wwidth, image_name), format='PNG')
                jpeg= buf.getvalue()

                #print "creo thumbnail"

                return jpeg

            except:
                pass

    ##### here return the image when doesn't find the requested image
    # ## set image name to default_image
    image_name = DEFAULT_IMAGE

    # ## getting variables
    orig = Image.open(image_name)
    width = int(orig.size[0])
    height = int(orig.size[1])
    max_width = int(handler.get_argument("mw", "{}".format(width)))

    # resampling image
    im = orig.resize((max_width,height * max_width / width), Image.ANTIALIAS)

    # convert pil image to bytes buffer
    buf= StringIO.StringIO()
    im.save(buf, format= 'PNG')
    jpeg= buf.getvalue()

    #print "retorna default"

    return jpeg

class ImageHandler(BaseHandler):

    def get(self, image_name):

        #setting headers
        self.set_header("Content-Type", "image/png")

        millis = int(round(time.time() * 1000))
        self.write(getIamgeBuffer(self, image_name))
        omillis = int(round(time.time() * 1000))

        # print "dif : {}".format(omillis - millis)

        self.finish()



class ImageHandler2(BaseHandler):

    def get(self):

        #setting headers
        self.set_header("Content-Type", "image/png")

        self.write(getIamgeBuffer(self, DEFAULT_IMAGE))
        self.finish()
        

class ImageDeleteHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        image_name = self.get_argument("image_name", "")
        tipo = self.get_argument("type","")
        identificador = self.get_argument("id","")

        print "files"
        if image_name != "":
            os.chdir( dir_img )

            for file in glob.glob("*" + image_name):
                try:
                    os.remove( file )
                except Exception, e:
                    print "no se elimino : {}".format( str(e) )
                    pass

            os.chdir("../../")

            if tipo == "timeline":
                try:
                    timeline = Timeline()
                    timeline.RemoveImage(identificador, image_name)
                except Exception,e:
                    print str( e )


            self.write("imagen eliminada")
        else:
            self.write( "imagen no existe " )