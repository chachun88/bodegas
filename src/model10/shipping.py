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
        self._edited = False
        self._price = 0
        self._correos_price = 0
        self._chilexpress_price = 0
        self._charge_type = 1

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

    @property
    def charge_type(self):
        return self._charge_type
    @charge_type.setter
    def charge_type(self, value):
        self._charge_type = value
    

    def List(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = '''\
                    select s.id,
                        c.name as origen, 
                        c2.name as destino, 
                        s.correos_price, 
                        s.chilexpress_price, 
                        s.price, 
                        s.edited, 
                        s.charge_type 
                    from "Shipping" s 
                    left join "City" c on c.id = s.from_city_id 
                    left join "City" c2 on c2.id = s.to_city_id
                    order by origen asc, destino asc'''
            cur.execute(query)
            lista = cur.fetchall()
            return self.ShowSuccessMessage(lista)
        except Exception,e:
            return self.ShowError(str(e))
        finally:
            cur.close()
            self.connection.close()

    def Save(self):

        if self.identifier != "":

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = '''update "Shipping" set from_city_id = %(from_city_id)s, to_city_id = %(to_city_id)s, correos_price = %(correos_price)s, chilexpress_price = %(chilexpress_price)s, price = %(price)s, edited = %(edited)s, charge_type = %(charge_type)s where id = %(id)s'''
            parameters = {
            "id":self.identifier,
            "from_city_id":self.from_city_id,
            "to_city_id":self.to_city_id,
            "correos_price":self.correos_price,
            "chilexpress_price":self.chilexpress_price,
            "price":self.price,
            "edited":self.edited,
            "charge_type":self.charge_type
            }

            try:
                # print cur.mogrify(query, parameters)
                cur.execute(query,parameters)
                self.connection.commit()
                return self.ShowSuccessMessage(self.identifier)
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                self.connection.close()
                cur.close()

        else:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = '''insert into "Shipping" (from_city_id,to_city_id,correos_price,chilexpress_price,price,edited,charge_type) values (%(from_city_id)s,%(to_city_id)s,%(correos_price)s,%(chilexpress_price)s,%(price)s,%(edited)s,%(charge_type)s) returning id'''
            parameters = {
            "from_city_id":self.from_city_id,
            "to_city_id":self.to_city_id,
            "correos_price":self.correos_price,
            "chilexpress_price":self.chilexpress_price,
            "price":self.price,
            "edited":self.edited,
            "charge_type":self.charge_type
            }

            try:
                cur.execute(query,parameters)
                self.identifier = cur.fetchone()["id"]
                self.connection.commit()
                return self.ShowSuccessMessage(self.identifier)
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                self.connection.close()
                cur.close()

    def Action(self,action):

        if action != "":

            if action == "correos_edited" or action == "chilexpress_edited":

                if action == "correos_edited":

                    cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                    query = '''update "Shipping" set price = correos_price where edited = false'''

                    try:
                        cur.execute(query)
                        self.connection.commit()
                        return self.ShowSuccessMessage("ok")
                    except Exception,e:
                        return self.ShowError(str(e))
                    finally:
                        self.connection.close()
                        cur.close()

                elif action == "chilexpress_edited":

                    cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                    query = '''update "Shipping" set price = chilexpress_price where edited = false'''

                    try:
                        cur.execute(query)
                        self.connection.commit()
                        return self.ShowSuccessMessage("ok")
                    except Exception,e:
                        return self.ShowError(str(e))
                    finally:
                        self.connection.close()
                        cur.close()

                else:

                    return self.ShowError("Acción seleccionada es inválida")

            else:

                cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                query = '''update "Shipping" set price = {action}'''.format(action=action)

                try:
                    cur.execute(query)
                    self.connection.commit()
                    return self.ShowSuccessMessage("ok")
                except Exception,e:
                    return self.ShowError(str(e))
                finally:
                    self.connection.close()
                    cur.close()

        else:

            return self.ShowError("Acción seleccionada es inválida")

    def InitById(self):

        if self.identifier == "":

            return self.ShowError("Debe especificar un identificador válido")

        else:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = '''select * from "Shipping" where id = %(id)s'''
            parameters = {
                "id":self.identifier
            }

            try:
                cur.execute(query,parameters)
                shipping = cur.fetchone()
                self.identifier = shipping["id"]
                self.from_city_id = shipping["from_city_id"]
                self.to_city_id = shipping["to_city_id"]
                self.edited = shipping["edited"]
                self.correos_price = shipping["correos_price"]
                self.chilexpress_price = shipping["chilexpress_price"]
                self.price = shipping["price"]
                self.charge_type = shipping["charge_type"]
                return self.ShowSuccessMessage(shipping)
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                self.connection.close()
                cur.close()


    def Remove(self):

        if self.identifier == 0:

            return self.ShowError("Debe especificador un identificador válido")

        else:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = '''delete from "Shipping" where id = %(id)s'''
            parameters = {
            "id":self.identifier
            }

            try:
                cur.execute(query,parameters)
                self.connection.commit()
                return self.ShowSuccessMessage(self.identifier)
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                self.connection.close()
                cur.close()

    def SaveTrackingCode(self, order_id="", tracking_code="", provider_id=""):

        if order_id == "":
            return self.ShowError("order id is empty")
        elif tracking_code == "":
            return self.ShowError("tracking_code of order {} is empty".format(order_id))
        elif provider_id == "":
            return self.ShowError("provider_id of order {} is empty".format(provider_id))
        else:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = '''update "Order" set tracking_code = %(tracking_code)s, provider_id = %(provider_id)s, state = 4 where id = %(order_id)s returning user_id'''
            parameters = {"tracking_code":tracking_code,"order_id":order_id,"provider_id":provider_id}

            try:
                cur.execute(query,parameters)
                self.connection.commit()
                user_id = cur.fetchone()["user_id"]
                return self.ShowSuccessMessage(user_id)
            except Exception, e:
                return self.ShowError("saving tracking code {}".format(str(e)))
            finally:
                cur.close()
                self.connection.close()

    def exists(self, from_city_id, to_city_id):

        if from_city_id == None:
            return self.ShowError("origen no puede estar vacio")
        elif to_city_id == None:
            return self.ShowError("destino no puede estar vacio")
        else:
            query = '''\
                    select id from "Shipping" 
                    where from_city_id = %(from_city_id)s 
                    and to_city_id = %(to_city_id)s'''
            parameters = {
                "from_city_id": from_city_id,
                "to_city_id": to_city_id
            }
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                cursor.execute(query, parameters)
                if cursor.rowcount > 0:
                    return self.ShowSuccessMessage(True)
                else:
                    return self.ShowSuccessMessage(False)
            except Exception, e:
                return self.ShowError("error al buscar precio de despacho, {}".format(
                    str(e)))
