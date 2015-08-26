#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basehandler import BaseHandler


class BannerHandler(BaseHandler):

    def get(self):

        pjax = bool(self.get_argument("_pjax", False))

        pjax_str = ''

        if pjax:
            pjax_str = '/ajax'

        self.render(
            "banner{}/index.html".format(pjax_str))
