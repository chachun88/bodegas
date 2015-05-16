#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from ..globals import *

from basehandler import BaseHandler

from bson import json_util

from ..model10.tag import Tag
from ..model10.product import Product

class TagHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.TAGS_LISTAR)

        page = self.get_argument("page",1)
        items = self.get_argument("items",20)

        tag = Tag()
        res = tag.List(page,items)

        if "success" in res:
            self.render("tag/list.html",lista=res["success"],dn="")
        else:
            self.render("tag/list.html",dn="error",mensaje=res["error"])

class RemoveTagHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        identificador = self.get_argument("id","")

        if identificador != "":

            tag = Tag()
            res = tag.Remove(int(identificador))

            if "success" in res:
                self.redirect("/tag/list")
            else:
                self.write(res["error"])
        else:
            self.write("identificador del tag está vacío")

class HideShowHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        identificador = self.get_argument("id","")
        tipo = self.get_argument("visible",0)

        if identificador != "" and tipo != "":
            
            tag = Tag()
            res = tag.HideShow(identificador,tipo)

            if "success" in res:
                self.redirect("/tag/list")
            else:
                self.write(res["error"])
        else:
            self.write("identificador del tag está vacío y/o operación no está definida")


class EditHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        identifier = self.get_argument("id","")

        # print identifier

        if identifier != "":

            tag = Tag()
            res = tag.InitById(identifier)
            # print res

            productos_asociados = tag.GetProductsByTagId(identifier)
            # print productos_asociados

            if "success" in productos_asociados:

                asociados = productos_asociados["success"]

                if "success" in res:
                    product = Product()
                    res_lista = product.GetList()
                    # print res_lista

                    if "success" in res_lista:
                        lista = res_lista["success"]

                        self.render("tag/save.html", tag=tag, mode="edit", product_list=lista, dn="", asociados=asociados)
                    else:
                        self.write(res_lista["error"])
                else:
                    self.write(res["error"])

            else:
                self.write(productos_asociados["error"])
        else:
            self.write("identificador del tag está vacío")


class AddHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        self.set_active(Menu.TAGS_ADD)

        tag = Tag()
        product = Product()
        lista = product.GetList()["success"]
        asociados = []
        self.render("tag/save.html", tag=tag, mode="add", product_list=lista, dn="", asociados=asociados)

    @tornado.web.authenticated
    def post(self):

        nombre = self.get_argument("name","").encode("utf-8")
        asociados_obj = [int(asociado.encode("utf-8")) for asociado in self.get_arguments("asociados")]
        # asociados_str = json_util.dumps(asociados_obj)
        identificador = self.get_argument("id","")

        if nombre == "" or len(asociados_obj) == 0:
            self.write("Debe llenar todos los campos del formulario")
        else:
            tag = Tag()
            tag.name = nombre
            tag.id = identificador

            save = tag.Save()

            if "success" in save:

                tag.id = save["success"]

                # print tag.id

                remove_asociation = tag.RemoveTagsAsociationByTagId(tag.id)

                if "success" in remove_asociation:

                    for product_id in asociados_obj:
                        response = tag.AddTagProduct(tag.id, product_id)
                        # self.write(response)

                        # if debugMode:
                        #     print response

                    self.redirect("/tag/list")

                else:

                    self.write(remove_asociation["error"])

            else:

                self.write(save["error"])

            # self.write("nombre:{} asociados:{} identificador:{}".format(nombre,asociados,identificador))
