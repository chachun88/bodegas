#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras


class Product_Size(BaseModel):

    def __init__(self):

        BaseModel.__init__(self)

        self._size_id = None
        self._product_sku = None

    @property
    def size_id(self):
        return self._size_id

    @size_id.setter
    def size_id(self, value):
        self._size_id = value

    @property
    def product_sku(self):
        return self._product_sku

    @product_sku.setter
    def product_sku(self, value):
        self._product_sku = value

    def save(self):

        res_exists = self.exists()

        if "success" in res_exists:

            if not res_exists["success"]:

                cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

                query = '''insert into "Product_Size" (product_sku, size_id) values (%(product_sku)s, %(size_id)s)'''
                parameters = {
                    "product_sku" : self.product_sku,
                    "size_id" : self.size_id
                }

                try:
                    cursor.execute(query, parameters)
                    self.connection.commit()
                    return self.ShowSuccessMessage("relation product size saved")
                except Exception, e:
                    return self.ShowError(str(e))
                finally:
                    self.connection.close()
                    cursor.close()
            else:
                return self.ShowSuccessMessage("relation already exists")
        else:
            return self.ShowError(res_exists["error"])

    def exists(self):

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select count(*) as cantidad from "Product_Size" where product_sku = %(product_sku)s and size_id = %(size_id)s'''
        parameters = {
            "product_sku" : self.product_sku,
            "size_id" : self.size_id
        }

        try:
            cursor.execute(query, parameters)
            cantidad = cursor.fetchone()["cantidad"]
            self.connection.commit()

            if cantidad > 0:
                return self.ShowSuccessMessage(True)
            else:
                return self.ShowSuccessMessage(False)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cursor.close()        
