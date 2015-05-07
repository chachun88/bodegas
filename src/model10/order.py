#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras
from cellar import Cellar
from order_detail import OrderDetail
from kardex import Kardex

class Order(BaseModel):

    ESTADO_PENDIENTE = 1  # rechazado si es webpay
    ESTADO_CONFIRMADO = 2
    ESTADO_PARA_DESPACHO = 3
    ESTADO_DESPACHADO = 4
    ESTADO_CANCELADO = 5

    @property
    def salesman(self):
        return self._salesman

    @salesman.setter
    def salesman(self, value):
        self._salesman = value

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, value):
        self._customer = value

    @property
    def subtotal(self):
        return self._subtotal

    @subtotal.setter
    def subtotal(self, value):
        self._subtotal = value

    @property
    def shipping(self):
        return self._shipping

    @shipping.setter
    def shipping(self, value):
        self._shipping = value

    @property
    def tax(self):
        return self._tax

    @tax.setter
    def tax(self, value):
        self._tax = value

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def town(self):
        return self._town

    @town.setter
    def town(self, value):
        self._town = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        self._city = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value

    @property
    def items_quantity(self):
        return self._items_quantity

    @items_quantity.setter
    def items_quantity(self, value):
        self._items_quantity = value

    @property
    def product_quantity(self):
        return self._product_quantity

    @product_quantity.setter
    def product_quantity(self, value):
        self._product_quantity = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def payment_type(self):
        return self._payment_type

    @payment_type.setter
    def payment_type(self, value):
        self._payment_type = value

    @property
    def billing_id(self):
        return self._billing_id

    @billing_id.setter
    def billing_id(self, value):
        self._billing_id = value

    @property
    def shipping_id(self):
        return self._shipping_id

    @shipping_id.setter
    def shipping_id(self, value):
        self._shipping_id = value

    def __init__(self):
        BaseModel.__init__(self)
        self.table = "Order"
        self._id = ""
        self._date = ""
        self._type = ""
        self._salesman = ""
        self._customer = ""
        self._subtotal = ""
        self._shipping = ""
        self._tax = ""
        self._total = ""
        self._address = ""
        self._town = ""
        self._city = ""
        self._source = ""
        self._country = ""
        self._items_quantity = ""
        self._product_quantity = ""
        self._state = ""
        self._payment_type = ""
        self._billing_id = ""
        self._shipping_id = ""

    def List(self, page, items):

        page = int(page)
        items = int(items)
        offset = (page - 1) * items
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query = '''select o.*,
                    coalesce(c.name, '') || ' ' || coalesce(c.lastname, '') as customer,
                    c.*,
                    ut.name as tipo_cliente,
                    o.id as order_id,
                    ct.name as city 
                    from "Order" o 
                    inner join "User" u on u.id = o.user_id 
                    inner join "Contact" c on c.id = o.billing_id 
                    inner join "City" ct on ct.id = c.city_id 
                    inner join "User_Types" ut on ut.id = u.type_id
                    order by o.id desc 
                    limit %(items)s 
                    offset %(offset)s'''

            parametros = {
                "items": items,
                "offset": offset
            }
            cur.execute(query, parametros)
            lista = cur.fetchall()
            return lista
        except Exception, e:
            print str(e)
            return {}

    def InitWithId(self, _id):

        # order = self.collection.find_one({"id":int(_id)})

        # if order:
        #     return json_util.dumps(order)
        # else:
        #     return "{}"

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select o.*,
                coalesce(c.name, '') || ' ' || coalesce(c.lastname, '') as customer,
                c.*,
                o.id as order_id,
                u.email, 
                ct.name as city 
                from "Order" o 
                inner join "User" u on u.id = o.user_id 
                inner join "Contact" c on c.id = o.billing_id 
                inner join "City" ct on ct.id = c.city_id 
                where o.id = %(id)s 
                limit 1'''

        parametros = {
            "id": _id
        }

        try:
            cur.execute(query, parametros)
            order = cur.fetchone()

            if cur.rowcount > 0:
                self.id                     = order["order_id"]
                self.date                   = order["date"]
                self.type                   = order["type"]
                self.telephone              = order["telephone"]
                self.customer               = order["customer"]
                self.subtotal               = order["subtotal"]
                self.shipping               = order["shipping"]
                self.tax                    = order["tax"]
                self.total                  = order["total"]
                self.address                = order["address"]
                self.town                   = order["town"]
                self.city                   = order["city"]
                self.source                 = order["source"]
                self.country                = order["country"]
                self.items_quantity         = order["items_quantity"]
                self.product_quantity       = order["products_quantity"]
                self.state                  = order["state"]
                self.payment_type           = order["payment_type"]
                self.billing_id             = order["billing_id"]
                self.shipping_id            = order["shipping_id"]
                self.customer_email         = order["email"]
                return self.ShowSuccessMessage(order)
            else:
                return self.ShowError("Pedido no encontrado")

        except Exception, e:
            return self.ShowError("Error al obtener el pedido, {}".format(str(e)))

    def Save(self):

        # new_id = db.seq.find_and_modify(query={'seq_name':'order_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]

        # validate contrains
        # object_id = self.collection.insert({
        #     "id": new_id,
        #     "date": self.date,
        #     "source": self.source,
        #     "country": self.country,
        #     "items_quantity": self.items_quantity,
        #     "product_quantity": self.product_quantity,
        #     "state": self.state,
        #     "salesman" : self.salesman,
        #     "customer" : self.customer,
        #     "subtotal" : self.subtotal,
        #     "shipping" : self.shipping,
        #     "tax" : self.tax,
        #     "total" : self.total,
        #     "address" : self.address,
        #     "town" : self.town,
        #     "city" : self.city,
        #     "type" : self.type
        #     })

        # return str(object_id)

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''insert into "Order" (date,source,items_quantity,state,user_id,subtotal,shipping,tax,total,type,products_quantity, payment_type, billing_id, shipping_id)'''
        query += ''' values(%(date)s,%(source)s,%(items_quantity)s,%(state)s,%(user_id)s,%(subtotal)s,%(shipping)s,%(tax)s,%(total)s,%(type)s,%(products_quantity)s%(payment_type)s,%(billing_id)s,%(shipping_id)s)'''
        query += ''' returning id'''

        parametros = {
            "date": self.date,
            "source": self.source,
            "items_quantity": self.items_quantity,
            "products_quantity": self.product_quantity,
            "state": self.state,
            "subtotal": self.subtotal,
            "shipping": self.shipping,
            "tax": self.tax,
            "total": self.total,
            "user_id": self.customer,
            "type": self.type,
            "payment_type": self.payment_type,
            "billing_id": self.billing_id,
            "shipping_id": self.shipping_id
        }

        cur.execute(query, parametros)

        self.id = cur.fetchone()["id"]

        return str(self.id)

    def DeleteOrder(self, identifier):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            query = '''delete from "Order_Detail" where order_id = %(order_id)s'''
            parameters = {"order_id": identifier}
            cur.execute(query, parameters)

            query = '''delete from "Order" where id = %(id)s'''
            parameters = {"id": identifier}
            cur.execute(query, parameters)

            self.connection.commit()
            return self.ShowSuccessMessage("orden {} eliminado correctamente".format(identifier))
        except Exception, e:
            self.connection.rollback()
            return self.ShowError("Error eliminando la orden {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

    def ChangeStateOrders(self, identifier, state):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''update "Order" set state = %(state)s where id = %(id)s'''
        parameters = {"id": identifier, "state": state}

        try:
            # print cur.mogrify(query, parameters)
            cur.execute(query, parameters)
            self.connection.commit()
            return self.ShowSuccessMessage("orden {} ha cambiado de estado exitosamente".format(identifier))
        except Exception, e:
            self.connection.rollback()
            return self.ShowError(str(e))
        finally:
            cur.close()
            self.connection.commit()

    def getTotalPages(self, items):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''select ceil(count(*)::float/%(items)s::float) as pages from "Order"'''
        parameters = {"items": items}

        try:
            cur.execute(query, parameters)
            pages = cur.fetchone()["pages"]
            return self.ShowSuccessMessage(pages)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()

    def cancel(self, identificador):

        cellar_id = None
        web_cellar = None

        cellar = Cellar()
        res_reservation_cellar = cellar.GetReservationCellar()

        errores = []

        if "success" in res_reservation_cellar:
            cellar_id = res_reservation_cellar["success"]
        else:
            return self.ShowError(res_reservation_cellar["error"])

        if identificador == "":
            return self.ShowError("identificador viene vacio")
        else:

            order = Order()
            res_order = order.InitWithId(identificador)

            cancelable = True

            if "success" in res_order:

                o = res_order["success"]

                if o["state"] != Order.ESTADO_CANCELADO and o["state"] != Order.ESTADO_DESPACHADO:

                    order_detail = OrderDetail()
                    details_res = order_detail.ListByOrderId(identificador)

                    if "success" in details_res:

                        details = details_res["success"]

                        # recorre cada producto del detalle de orden y determina si la orden es cancelable
                        for d in details:

                            k = Kardex()
                            find_kardex = k.FindKardex(d["sku"], cellar_id, d['size_id'])
                            units = 0

                            if "success" in find_kardex:
                                units = k.balance_units  

                            if int(units) < int(d['quantity']): 

                                cancelable = False

                        # end for

                        # si no es cancelable la orden se guarda en el array identificadores para avisar al usuario
                        if not cancelable:
                            errores.append("Pedido {} no es posible devolver stock a bodega".format(identificador))
                        else:

                            cellar = Cellar()
                            res_web_cellar = cellar.GetWebCellar()

                            if "success" in res_web_cellar:

                                web_cellar = res_web_cellar["success"]

                            # mueve c/u de los productos desde la bodega de reserva a la bodega web
                            kardex = Kardex()
                            res = kardex.moveOrder(details, web_cellar, cellar_id)

                            if "error" in res:
                                errores.append("error en el pedido {}, {}".format(identificador, res["error"]))
                    else:
                        return self.ShowError(details_res["error"])
                elif o["state"] == Order.ESTADO_DESPACHADO:
                    return self.ShowError("Pedido {} no puede ser cancelado, ya que se encuentra despachado".format(identificador))
                else:
                    return self.ShowError("Pedido {} ya esta cancelado".format(identificador))
            else:
                return self.ShowError(res_order)

            if len(errores) > 0:
                return self.ShowError(errores)
            else:
                return self.ShowSuccessMessage("ok")
