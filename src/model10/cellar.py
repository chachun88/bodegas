#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
# from bson.objectid import ObjectId

from kardex import Kardex
from product import Product
from size import Size

from bson import json_util

import psycopg2
import psycopg2.extras

import time
import datetime

import re


class Cellar(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self.name = ''
        self.description = ''
        self.table = 'Cellar'
        self.city = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def for_sale(self):
        return self._for_sale

    @for_sale.setter
    def for_sale(self, value):
        self._for_sale = value

    # override
    def Remove(self):

        is_empty = True

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Kardex" where cellar_id = %(cellar_id)s'''

        parametros = {
            "cellar_id": self.id
        }

        cur.execute(query, parametros)

        kardex = cur.fetchall()

        for k in kardex:

            query = '''select * from "Kardex" where product_sku = %(product_sku)s and cellar_id = %(cellar_id)s and size_id = %(size_id)s order by date desc, id desc limit 1'''

            parametros = {
                "product_sku": k["product_sku"],
                "cellar_id": self.id,
                "size_id": k["size_id"]
            }

            cur.execute(query, parametros)

            _kardex = cur.fetchone()

            if _kardex:
                if int(_kardex["balance_units"]) >= 1:
                    is_empty = False

        if is_empty:

            query = '''update "User" set cellar_permissions = cellar_permissions - array[%(cellar_id)s]'''
            parametros = {
                "cellar_id": self.id
            }

            cur.execute(query, parametros)
            self.connection.commit()

            return BaseModel.Remove(self)

        else:
            return self.ShowError("No se puede eliminar, aún contiene productos.")

    def GetTotalUnits(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select distinct product_sku, size_id from "Kardex" k where k.cellar_id = %(id)s'''
        parametros = {
            "id": self.id
        }
        cur.execute(query, parametros)
        pproduct_sku = cur.fetchall()

        kardex = Kardex()
        total_units = 0

        for p in pproduct_sku:

            response = kardex.FindKardex(
                p["product_sku"], self.id, p["size_id"])

            if "success" in response:
                total_units += kardex.balance_units
            # else:
            #     print response["error"]

        return int(total_units)

    def GetTotalPrice(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select distinct product_sku, size_id from "Kardex" where cellar_id = %(id)s'''
        parametros = {
            "id": self.id
        }
        cur.execute(query, parametros)
        pproduct_sku = cur.fetchall()

        kardex = Kardex()
        total_price = 0

        for p in pproduct_sku:

            response = kardex.FindKardex(
                p["product_sku"], self.id, p["size_id"])

            if "success" in response:
                total_price += kardex.balance_total
            # else:
            #     print response["error"]

        return int(total_price)

    #@return json
    def Print(self):

        me = {"id": self.id,
              "name": self.name,
              "description": self.description,
              "for_sale": self.for_sale,
              "total_price": self.GetTotalPrice(),
              "total_units": self.GetTotalUnits()}

        return me

    @staticmethod
    def CellarExists(cellar_name):

        bm = BaseModel()

        cur = bm.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Cellar" where name = %(name)s limit 1'''
        parametros = {
            "name": cellar_name
        }

        cur.execute(query, parametros)

        if cur.rowcount > 0:
            return True
        else:
            return False

    # validates and save cellar, it could be validated by name
    def Save(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Cellar" where name = %(name)s limit 1'''
        parametros = {
            "name": self.name
        }
        cur.execute(query, parametros)
        cellar = cur.fetchone()

        if cellar:

            try:
                query = '''update "Cellar" set description = %(description)s, name = %(name)s, city_id = %(city)s where id = %(id)s returning id'''
                parametros = {
                    "description": self.description,
                    "name": self.name,
                    "id": cellar['id'],
                    "city": self.city
                }
                cur.execute(query, parametros)
                self.connection.commit()
                self.id = cur.fetchone()[0]
                self.InitById(self.id)

                return self.ShowSuccessMessage(self.id)

            except Exception, e:
                return self.ShowError("failed to update cellar {}, error:{}".format(self.name, str(e)))

        else:

            try:
                query = '''insert into "Cellar" (description, name,city_id) values (%(description)s,%(name)s,%(city_id)s) returning id'''
                parametros = {
                    "description": self.description,
                    "name": self.name,
                    "city_id": self.city
                }
                cur.execute(query, parametros)
                self.connection.commit()
                self.id = cur.fetchone()[0]
                self.InitById(self.id)

                return self.ShowSuccessMessage(self.id)

            except Exception, e:
                return self.ShowError("failed to save cellar {}, error:{}".format(self.name, str(e)))

    def List(self, page, items):

        page = int(page)
        items = int(items)
        offset = items * (page - 1)

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Cellar" order by name limit %(items)s offset %(offset)s'''
        parametros = {
            "items": items,
            "offset": offset
        }

        cur.execute(query, parametros)
        cellars = cur.fetchall()

        data_rtn = []  # return this data

        for d in cellars:

            cellar = Cellar()
            cellar.id = d["id"]
            cellar.name = d["name"]
            cellar.description = d["description"]
            cellar.city = d["city_id"]
            cellar.for_sale = d["for_sale"]

            data_rtn.append(cellar.Print())

        return data_rtn

        # return json_util.dumps(cellars)

    #  WARNING: this method is not opmitimized
    #@return direct database collection
    @staticmethod
    def GetAllCellars():

        conn = BaseModel().connection
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Cellar"'''

        try:
            cur.execute(query)
            cellar = cur.fetchall()

            data_rtn = []

            for c in cellar:
                cellar = Cellar()
                cellar.id = c['id']
                cellar.name = c['name']
                cellar.description = c['description']
                cellar.city = c["city_id"]
                cellar.for_sale = c["for_sale"]

                data_rtn.append(cellar.Print())

            return data_rtn

        except Exception, e:
            print "Get all cellars {}".format(str(e))
        finally:
            conn.close()
            cur.close()

    def InitByName(self, name):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Cellar" where name = %(name)s limit 1'''
        parametros = {
            "name": name
        }
        cur.execute(query, parametros)

        if cur.rowcount > 0:

            cellar = cur.fetchone()

            self.id = cellar['id']
            self.name = cellar['name']
            self.description = cellar['description']
            self.city = cellar["city_id"]
            self.for_sale = cellar["for_sale"]
            return self.ShowSuccessMessage("cellar initialized")

        else:

            return self.ShowError("no existe la bodega {}".format(name))

    def InitById(self, idd):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Cellar" where id = %(id)s limit 1'''
        parametros = {
            "id": idd
        }

        try:
            cur.execute(query, parametros)
            cellar = cur.fetchone()

            if cur.rowcount > 0:
                self.id = cellar['id']
                self.name = cellar['name']
                self.description = cellar['description']
                self.city = cellar["city_id"]
                self.for_sale = cellar["for_sale"]
                return self.ShowSuccessMessage("cellar initialized")

            else:

                return self.ShowError("item not found")
        except Exception, e:
            return self.ShowError("cellar not found, {}".format(str(e)))
        finally:
            self.connection.close()
            cur.close()

    def ListProducts(self, page=1, items=30):

        rtn_data = []

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select distinct product_sku, size_id from "Kardex" where cellar_id = %(id)s order by product_sku, size_id'''
        parametros = {
            "id": self.id
        }
        cur.execute(query, parametros)
        pproduct_sku = cur.fetchall()

        kardex = Kardex()

        for p in pproduct_sku:
            product = Product()
            # print "SKU:{}".format(p["product_sku"])
            response_obj = product.InitBySku(p["product_sku"])

            if "error" not in response_obj:

                prod_print = response_obj["success"]

                response_obj = kardex.FindKardex(
                    p["product_sku"], self.id, p["size_id"])

                if "success" in response_obj:

                    size = Size()
                    size.id = kardex.size_id

                    res_size_id = size.initById()

                    if "success" in res_size_id:

                        prod_print["balance_units"] = kardex.balance_units
                        prod_print["balance_price"] = kardex.balance_price
                        prod_print["balance_total"] = kardex.balance_total
                        prod_print["size_id"] = kardex.size_id
                        prod_print["size"] = size.name

                        rtn_data.append(prod_print)

                    # else:
                    #     return res_size_id

                else:
                    return response_obj

            else:
                return response_obj

        return {"success": rtn_data}

    def ListKardex(self, day, fromm, until):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if day == "today":
            # now = datetime.datetime.now()
            # yesterday = now - datetime.timedelta(days=1)
            query = """select k.*, c.name, s.name as size from "Kardex" k 
                    inner join "Cellar" c on c.id = k.cellar_id 
                    inner join "Size" s on s.id = k.size_id
                    where date(date) = DATE 'today'"""
        if day == "yesterday":
            # now = datetime.datetime.now() - datetime.timedelta(days=1)
            # yesterday = now - datetime.timedelta(days=2)
            query = """select k.*, c.name, s.name as size from "Kardex" k 
                    inner join "Cellar" c on c.id = k.cellar_id 
                    inner join "Size" s on s.id = k.size_id
                    where date(date) = DATE 'yesterday'"""

        if day == "today" or day == "yesterday":

            # start_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
            # end_date = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
            # oid_start = ObjectId.from_datetime(start_date)
            # oid_stop = ObjectId.from_datetime(end_date)

            # str_query = '{ "$and" : [{"operation_type":"sell"},{ "_id" : { "$gte" : { "$oid": "%s" }, "$lt" : { "$oid": "%s" } } }]}' % ( str(oid_start), str(oid_stop) )

            query += """ and operation_type = 'sell'"""
            # data = db.kardex.find( json_util.loads(str_query) )
            cur = self.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(query)
            data = cur.fetchall()

            return data

        if day == "period":

            # ffrom=fromm.split("-")

            # from_y=int(ffrom[0])
            # from_m=int(ffrom[1])
            # from_d=int(ffrom[2])

            # untill= until.split("-")

            # until_y=int(untill[0])
            # until_m=int(untill[1])
            # until_d=int(untill[2])

            # now = datetime.datetime.now()
            # yesterday = now - datetime.timedelta(days=30)

            # start_date = datetime.datetime(from_y, from_m, from_d, 0, 0, 0)
            # end_date = datetime.datetime(until_y, until_m, until_d, 23, 59, 59)
            # oid_start = ObjectId.from_datetime(start_date)
            # oid_stop = ObjectId.from_datetime(end_date)

            # str_query = '{ "$and" : [{"operation_type":"sell"},{ "_id" : { "$gte" : { "$oid": "%s" }, "$lt" : { "$oid": "%s" } } }]}' % ( str(oid_start), str(oid_stop) )
            # data = db.kardex.find( json_util.loads(str_query) )
            # return data

            query = """select k.*, c.name, s.name as size from "Kardex" k 
                    inner join "Cellar" c on c.id = k.cellar_id 
                    inner join "Size" s on s.id = k.size_id
                    where date(date) between %(start_date)s and %(end_date)s and operation_type = 'sell'"""
            parameters = {
                "start_date": fromm,
                "end_date": until
            }
            cur = self.connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(query, parameters)
            data = cur.fetchall()
            return data

    def FindProductKardex(self, product_sku, cellar_identifier, size_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if cellar_identifier == "remove" and size_id == "remove":

            query = '''\
                    select coalesce(sum(balance_units),0) as total 
                    from (select distinct on(cellar_id, size_id) balance_units 
                            from "Kardex" where product_sku = %(product_sku)s 
                            order by cellar_id, size_id, date desc) as t'''
            parametros = {
                "product_sku": product_sku
            }

            try:
                cur.execute(query, parametros)
                result = cur.fetchone()
                return self.ShowSuccessMessage(result["total"])
            except Exception, e:
                return self.ShowError("get total by sku and size, {}".format(str(e)))
            finally:
                self.connection.close()
                cur.close()
        else:

            query = '''select sum(units) as total, operation_type from "Kardex" where product_sku = %(product_sku)s and cellar_id = %(cellar_id)s and size_id = %(size_id)s group by operation_type'''
            parametros = {
                "product_sku": product_sku,
                "cellar_id": cellar_identifier,
                "size_id": size_id
            }

            print cur.mogrify(query, parametros)

            try:
                cur.execute(query, parametros)
                result = cur.fetchall()
                return self.ShowSuccessMessage(result)
            except Exception, e:
                return self.ShowError("get total by sku and size, {}".format(str(e)))
            finally:
                self.connection.close()
                cur.close()

    def Rename(self, new_name):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:

            if new_name == "":
                raise

            query = '''update "Cellar" set name = %(name)s where id = %(id)s'''
            parametros = {
                "name": new_name,
                "id": self.id
            }

            cur.execute(query, parametros)
            self.connection.commit()
            self.name = new_name
            self.ShowSuccessMessage("name changed correctly")
        except:
            self.ShowError("error changing name")

    def SelectForSale(self, cellar_id):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = '''update "Cellar" set for_sale = 0'''
            cur.execute(query)

            query = '''update "Cellar" set for_sale = 1 where id = %(id)s'''
            parameters = {
                "id": cellar_id
            }
            cur.execute(query, parameters)
            self.connection.commit()
            return self.ShowSuccessMessage(cellar_id)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()

    def GetWebCellar(self):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = '''select id from "Cellar" where for_sale = 1 limit 1'''
            cur.execute(query)
            cellar = cur.fetchone()["id"]
            return self.ShowSuccessMessage(cellar)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()

    def GetReservationCellar(self):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = '''select id from "Cellar" where reservation = 1 limit 1'''
            cur.execute(query)
            cellar = cur.fetchone()["id"]
            return self.ShowSuccessMessage(cellar)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()

    def SelectReservation(self, cellar_id):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = '''update "Cellar" set reservation = 0'''
            cur.execute(query)

            query = '''update "Cellar" set reservation = 1 where id = %(id)s'''
            parameters = {
                "id": cellar_id
            }
            cur.execute(query, parameters)
            self.connection.commit()
            return self.ShowSuccessMessage(cellar_id)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()

    def FindById(self, id_list):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select * from "Cellar" where id = any(%(id_list)s)'''
        parameters = {
            "id_list": id_list
        }

        try:
            # print cur.mogrify(query, parameters)
            cur.execute(query, parameters)
            self.connection.commit()
            cellars = cur.fetchall()
            return self.ShowSuccessMessage(cellars)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()
