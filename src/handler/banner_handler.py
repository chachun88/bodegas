#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basehandler import BaseHandler
from bson import json_util
from src.model10.banner import Banner
from src.globals import *


class BannerHandler(BaseHandler):

    def get(self):

        pjax = bool(self.get_argument("_pjax", False))

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        self.render("banner{}/index.html".format(pjax_str), url_local=url_local)

    def post(self):

        banner1 = self.save('banner1', self.get_argument("banner1", ""))
        banner2 = self.save('banner2', self.get_argument("banner2", ""))
        banner3 = self.save('banner3', self.get_argument("banner3", ""))

        banner1_movil = self.save('banner1_movil', self.get_argument("banner1_movil", ""))
        banner2_movil = self.save('banner2_movil', self.get_argument("banner2_movil", ""))
        banner3_movil = self.save('banner3_movil', self.get_argument("banner3_movil", ""))

        caluga_video = self.save('caluga_video', self.get_argument("caluga_video", ""))

        caluga_ir_tienda = self.save('caluga_ir_tienda', self.get_argument("tienda-caluga", ""))
        caluga_nuevo = self.save('caluga_nuevo', self.get_argument("nuevo-caluga", ""))
        instagram = self.save('instagram', self.get_argument("instagram", ""))
        historia = self.save('historia', self.get_argument("historia", ""))
        registro = self.save('registro', self.get_argument("registro", ""))
        mayorista = self.save('mayorista', self.get_argument("mayorista", ""))
        background_registro = self.save('background_registro', self.get_argument("background_registro", ""))
        background_mayorista = self.save('background_mayorista', self.get_argument("background_mayorista", ""))

        nuevo = self.save('nuevo', self.get_argument("nuevo", ""))
        sale = self.save('sale', self.get_argument("sale", ""))
        tienda = self.save('tienda', self.get_argument("tienda", ""))
        background_footer_izq = self.save('background_footer_izq', self.get_argument("background_footer_izq", ""))
        background_footer_der = self.save('background_footer_der', self.get_argument("background_footer_der", ""))
        background_header = self.save('background_header', self.get_argument("background_header", ""))

        self.redirect("/banner")

    def save(self, name, json):

        banner = Banner()
        banner.initByName(name)
        banner.name = name
        banner.image = self.getImageUrl(json)
        banner.thumbnail = self.getThumbnail(json)

        banner.save()

    def getImageUrl(self, json):

        if json == "":
            return ""
        else:
            obj = json_util.loads(json)
            return obj["image"]

    def getThumbnail(self, json):

        if json == "":
            return ""
        else:
            obj = json_util.loads(json)
            return obj["thumb_200"]
