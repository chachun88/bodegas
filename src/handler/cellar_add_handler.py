#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from ..globals import Menu

from basehandler import BaseHandler

from ..model10.cellar import Cellar
from ..model10.user import User
from ..model10.city import City


class CellarAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_active(Menu.BODEGAS_AGREGAR) # change menu active item
        pjax = bool(self.get_argument("_pjax", False))
        city = City()
        cities = city.List()
        pjax_str = ''
        if pjax:
            pjax_str = '/ajax'
        self.render("cellar{}/add.html".format(pjax_str), side_menu=self.side_menu,cities=cities["success"])

    @tornado.web.authenticated
    def post(self):

        name = self.get_argument("name", "bodega sin nombre").encode("UTF-8")
        description = self.get_argument("description", "").encode("UTF-8")
        city = self.get_argument("city",0)

        cellar = Cellar()
        cellar.name = name
        cellar.description = description
        cellar.city = city

        bodega = cellar.CellarExists(name)

        if bodega == False:
            cellar.Save()

            ## trying to add current cellar permissions to current user
            try:
                user = User()
                user.InitWithEmail( self.get_current_user() )

                self.write(cellar.name)

                if cellar.name not in user.permissions:
                    user.permissions.append( cellar.name )
                    user.Save()

            except Exception, e:
                self.write("exception : {}".format( e ) )

            self.redirect("/cellar?dn=t")
        else:
            self.redirect("/cellar?dn=dnt")
        