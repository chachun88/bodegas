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


class ImageHandler(BaseHandler):

    def __getDefaultImage(self, max_width):
        # here return the image when doesn't find the requested image
        # set image name to default_image
        image_name = DEFAULT_IMAGE

        # getting variables
        orig = Image.open(image_name)
        width = int(orig.size[0])
        height = int(orig.size[1])

        if max_width == -1:
            max_width = width

        # resampling image
        im = orig.resize((max_width,height * max_width / width), Image.ANTIALIAS)

        # convert pil image to bytes buffer
        buf = StringIO.StringIO()
        im.save(buf, format='PNG')
        jpeg = buf.getvalue()

        # print "retorna default"

        return jpeg

    def __getFullImage(self, image_name):
        """
        return full image, if not found returns default image
        """
        try:
            image_path = dir_img + image_name
            f = open(image_path, "rb")
            buff = f.read()
            f.close()

            return buff
        except:
            return self.__getDefaultImage(max_width)

    def __createMaxWidthImage(self, image_name, max_width):
        try:
            # image doesnt exist so i create it
            # image_path = dir_img + "{}{}".format(max_width, image_name)

            # getting variables
            orig = Image.open( dir_img + image_name)
            width = int(orig.size[0])
            height = int(orig.size[1])

            if max_width == -1:
                max_width = width

            # resampling image
            im = orig.resize((max_width,height * max_width / width), Image.ANTIALIAS)

            # convert pil image to bytes buffer
            buf = StringIO.StringIO()
            im.save(buf, format='PNG')
            im.save( dir_img + "{}{}".format(max_width, image_name), format='PNG')
            jpeg = buf.getvalue()

            return jpeg

        except:
            return self.__getDefaultImage(max_width)

    def __getMaxWidthImage(self, image_name, max_width):
        # show scaled image
        try:  # detect if image exist
            f = open( dir_img + "{}{}".format(max_width, image_name), "rb")
            buff = f.read()
            f.close()

            return buff
        except:

            # if the image doent exists, try to create a new one
            return self.__createMaxWidthImage(image_name, max_width)

    def __getMaxWidthMinHeightImage(self, image_name, max_width, min_height):
        return self.__getMaxWidthImage(image_name, max_width)

    def getImageBuffer(self, image_name, max_width=-1, min_height=-1):

        # case 1: user ask for full image
        if max_width == -1 and min_height == -1:

            # show full image or default image
            return self.__getFullImage(image_name)

        # case 2: user wish to force width but height
        elif min_height == -1:
            return self.__getMaxWidthImage(image_name, max_width)

        # case 3: user want max_width and min_heihgt
        else:

            return self.__getMaxWidthMinHeightImage(image_name, max_width, min_height)

        return self.__getDefaultImage(self, max_width)

    def get(self, image_name):

        max_width = int(self.get_argument('mw', -1))

        # setting headers
        self.set_header("Content-Type", "image/png")
        self.write(self.getImageBuffer(image_name, max_width=max_width))
        self.finish()


class ImageDafitiHandler(ImageHandler):

    def get(self, image_name):

        # xml doesnt allow &
        wh = self.get_argument("mwh", "-1,-1")  # pair of max_width and min_height

        max_width = int(wh.split(","))[0]
        min_height = int(wh.split(","))[1]

        self.set_header("Content-Type", "image/png")
        self.write(
            self.getImageBuffer(
                image_name, max_width=max_width, min_height=min_height))


class ImageHandler2(ImageHandler):

    def get(self):

        max_width = int(self.get_argument('mw', -1))

        # setting headers
        self.set_header("Content-Type", "image/png")

        self.write(self.getImageBuffer(DEFAULT_IMAGE, max_width=max_width))
        self.finish()


class ImageDeleteHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        image_name = self.get_argument("image_name", "")
        tipo = self.get_argument("type","")
        identificador = self.get_argument("id","")

        # print "files"
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
