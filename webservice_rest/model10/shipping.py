#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras
# from bson.objectid import ObjectId

class Shipping(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.table = 'Shipping'
        self._identifier = 0
        self._to_city_id = 0
        self._from_city_id = 0
        self._edited = 0
        self._price = 0
        self._correos_price = 0
        self._chilexpress_price = 0

    @property
    def identifier(self):
        return self._identifier
    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def from_city_id(self):
        return self._from_city_id
    @from_city_id.setter
    def from_city_id(self, value):
        self._from_city_id = value

    @property
    def to_city_id(self):
        return self._to_city_id
    @to_city_id.setter
    def to_city_id(self, value):
        self._to_city_id = value

    @property
    def correos_price(self):
        return self._correos_price
    @correos_price.setter
    def correos_price(self, value):
        self._correos_price = value

    @property
    def chilexpress_price(self):
        return self._chilexpress_price
    @chilexpress_price.setter
    def chilexpress_price(self, value):
        self._chilexpress_price = value

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        self._price = value
    

    @property
    def edited(self):
        return self._edited
    @edited.setter
    def edited(self, value):
        self._edited = value

    def List(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            cur.execute('''select s.id,c.name as origen, c2.name as destino, s.correos_price, s.chilexpress_price, s.price from "Shipping" s left join "City" c on c.id = s.from_city_id left join "City" c2 on c2.id = s.to_city_id''')
            lista = cur.fetchall()
            return self.ShowSuccessMessage(lista)
        except Exception,e:
            return self.ShowError(str(e))
        finally:
            cur.close()
            self.connection.close()

    def Save(self):

        if int(self.identifier) != 0:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = '''update "Shipping" set from_city_id = %(from_city_id)s, to_city_id = %(from_city_id)s, correos_price = %(correos_price)s, chilexpress_price = %(chilexpress_price)s, price = %(price)s, edited = %(edited)s where id = %(id)s'''
            parameters = {
            "id":self.id,
            "from_city_id":self.from_city_id,
            "to_city_id":self.to_city_id,
            "correos_price":self.correos_price,
            "chilexpress_price":self.chilexpress_price,
            "price":self.price,
            "edited":self.edited
            }

            try:
                cur.execute(query,parameters)
                self.connection.commit()
                return self.ShowSuccessMessage(self.id)
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                self.connection.close()
                cur.close()

        else:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = '''insert into "Shipping" (from_city_id,to_city_id,correos_price,chilexpress_price,price,edited) values (%(from_city_id)s,%(to_city_id)s,%(correos_price)s,%(chilexpress_price)s,%(price)s,%(edited)s) returning id'''
            parameters = {
            "from_city_id":self.from_city_id,
            "to_city_id":self.to_city_id,
            "correos_price":self.correos_price,
            "chilexpress_price":self.chilexpress_price,
            "price":self.price,
            "edited":self.edited
            }

            try:
                cur.execute(query,parameters)
                self.id = cur.fetchone()["id"]
                self.connection.commit()
                return self.ShowSuccessMessage(self.id)
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                self.connection.close()
                cur.close()




