#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras
from bson import json_util

class Tag(BaseModel):

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    

    def __init__(self):
        BaseModel.__init__(self)
        self.table = "Tag"

    def Save(self):

        

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # existe = False

        query = '''select id from "Tag" where name = %(name)s'''
        parameters = {
        "name":self.name
        }

        try:
            cur.execute(query,parameters)

            if cur.rowcount > 0:
                self.id = cur.fetchone()["id"]
            # else:
            #     print "self.id: {}".format(self.id)

        except Exception,e:
            self.connection.close()
            cur.close()
            return self.ShowError("Error al comprobar existencia del tag, {}".format(str(e)))

        if self.id == "":

            query = '''insert into "Tag" (name) values (%(name)s) returning id'''
            parameters = {
            "name":self.name
            }

            try:
                cur.execute(query,parameters)
                self.connection.commit()
                self.id = cur.fetchone()["id"]
                return self.ShowSuccessMessage(self.id)
            except Exception,e:
                return self.ShowError("Error saving tag: {}".format(str(e)))
            finally:
                self.connection.close()
                cur.close()


        else:

            # print "AQQQQQQ"

            query = '''update "Tag" set name = %(name)s where id = %(id)s returning id'''
            parameters = {
            "name":self.name,
            "id":self.id
            }

            try:
                cur.execute(query,parameters)
                self.id = cur.fetchone()["id"]
                self.connection.commit()
                return self.ShowSuccessMessage(self.id)
            except Exception,e:
                return self.ShowError("Error updating tag: {}".format(str(e)))
            finally:
                self.connection.close()
                cur.close()


    def GetTagsByIds(self,ids):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select * from "Tag" where id = any(%(ids)s)'''
        parameters = {
        "ids":ids
        }

        try:
            cur.execute(query,parameters)
            tags = cur.fetchall()
            return self.ShowSuccessMessage(tags)
        except Exception,e:
            return self.ShowError("Error al buscar tags por id: {}".format(str(e)))
        finally:
            self.connection.close()
            cur.close()

    def GetTagsByProductId(self,_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select * from "Tag" t left join "Tag_Product" tp on tp.tag_id = t.id where tp.product_id = %(id)s'''
        parameters = {
        "id":_id
        }

        try:
            cur.execute(query,parameters)
            tags = cur.fetchall()
            return self.ShowSuccessMessage(tags)
        except Exception,e:
            return self.ShowError("Error al buscar tags por product_id: {}".format(str(e)))
        finally:
            self.connection.close()
            cur.close()

    def AddTagProduct(self,tag_id,product_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''insert into "Tag_Product" (tag_id,product_id) values (%(tag_id)s,%(product_id)s) returning id'''
        parameters = {
        "tag_id":tag_id,
        "product_id":product_id
        }

        try:
            cur.execute(query,parameters)
            identifier = cur.fetchone()["id"]
            self.connection.commit()
            return self.ShowSuccessMessage(str(identifier))
        except Exception,e:
            return self.ShowError("Error agregando relacion tag y producto, {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

        
    def RemoveTagsAsociation(self,product_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''delete from "Tag_Product" where product_id = %(product_id)s'''
        parameters = {"product_id":product_id}

        try:
            cur.execute(query,parameters)
            self.connection.commit()
            return self.ShowSuccessMessage("Asociaciones al producto {} se han borrado correctamente".format(product_id))
        except Exception,e:
            return self.ShowError("Error eliminando relacion tag y producto, {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()
        
    def List(self,page=1,items=20):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        limit = int(items)
        page = int(page)
        offset = (page-1) * limit

        query = '''select * from "Tag" limit %(limit)s offset %(offset)s'''
        parameters = {
        "limit":limit,
        "offset":offset
        }

        try:
            cur.execute(query,parameters)
            lista = cur.fetchall()
            return self.ShowSuccessMessage(lista)
        except Exception,e:
            return self.ShowError("Error al obtener lista de tags, {}".format(str(e)))

    def RemoveTagsAsociationByTagId(self,tag_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''delete from "Tag_Product" where tag_id = %(tag_id)s'''
        parameters = {"tag_id":tag_id}

        try:
            cur.execute(query,parameters)
            self.connection.commit()
            return self.ShowSuccessMessage("Asociaciones al tag {} se han borrado correctamente".format(tag_id))
        except Exception,e:
            return self.ShowError("Error eliminando relacion tag y producto, {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

    def InitById(self,identificador=""):

        if identificador != "":

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = '''select * from "Tag" where id = %(identificador)s'''
            parameters = {"identificador":identificador}

            try:
                cur.execute(query,parameters)
                tag = cur.fetchone()
                return self.ShowSuccessMessage(tag)
            except Exception,e:
                return self.ShowError("Error al inicializar tag por id, {}".format(str(e)))

        else:

            return self.ShowError("Identificador viene vacío")


    def GetProductsByTagId(self,_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select product_id from "Tag" t left join "Tag_Product" tp on tp.tag_id = t.id where tp.tag_id = %(id)s'''
        parameters = {
        "id":_id
        }

        lista_product_id = []

        try:
            cur.execute(query,parameters)
            tags = cur.fetchall()

            for t in tags:
                lista_product_id.append(t["product_id"])

            return self.ShowSuccessMessage(lista_product_id)
        except Exception,e:
            return self.ShowError("Error al buscar tags por tag_id: {}".format(str(e)))
        finally:
            self.connection.close()
            cur.close()

    def HideShow(self,tag_id,visible):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''update "Tag" set visible = %(visible)s where id = %(id)s'''
        parameters = {
        "visible":visible,
        "id":tag_id
        }

        try:
            cur.execute(query,parameters)
            self.connection.commit()
            return self.ShowSuccessMessage(tag_id)
        except Exception,e:
            return self.ShowError(str(e))

    
