#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

from bson import json_util

import psycopg2
import psycopg2.extras

class Size(BaseModel):

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    

    def __init__(self):
        BaseModel.__init__(self)
        self._name = ''


    def initById(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Size" where id = %(id)s limit 1'''

        parametros = {
            "id": self.id
        }

        try:
            cur.execute(query,parametros)

            if cur.rowcount > 0:
                
                talla = cur.fetchone()
                self.name = talla["name"]

                return self.ShowSuccessMessage(talla)

            else:

                return self.ShowError("Size is not found")

        except Exception, e:

            return self.ShowError("Size initialization, {}".format(str(e)))

        finally:

            cur.close()
            self.connection.close()


    def list(self):
        
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Size"'''

        try:
            cur.execute(query)

            if cur.rowcount > 0:
                
                tallas = cur.fetchall()

                return self.ShowSuccessMessage(tallas)

            else:

                return self.ShowError("No sizes found")

        except Exception, e:

            return self.ShowError("Finding sizes, {}".format(str(e)))

        finally:

            cur.close()
            self.connection.close()

    def initByName(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Size" where name = %(name)s limit 1'''

        parametros = {
            "name": self.name
        }

        try:
            cur.execute(query,parametros)

            if cur.rowcount > 0:
                
                talla = cur.fetchone()
                self.id = talla["id"]

                return self.ShowSuccessMessage(talla)

            else:

                return self.insert()

        except Exception, e:

            return self.ShowError("Size initialization, {}".format(str(e)))

        finally:

            cur.close()
            self.connection.close()

    def insert(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''insert into "Size" (name) values (%(name)s) returning id'''

        parametros = {
            "name": self.name
        }

        try:
            cur.execute(query,parametros)
            self.connection.commit()
                
            talla = cur.fetchone()
            self.id = talla["id"]

            return self.ShowSuccessMessage("Size have been successfully created")

        except Exception, e:

            return self.ShowError("Size creation, {}".format(str(e)))

        finally:

            cur.close()
            self.connection.close()
