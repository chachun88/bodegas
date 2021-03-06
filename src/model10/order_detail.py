#!/usr/bin/env python

from basemodel import BaseModel
import psycopg2
import psycopg2.extras


class OrderDetail(BaseModel):

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def order_id(self, value):
        self._order_id = value

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def __init__(self):
        BaseModel.__init__(self)
        self._id = ""
        self._order_id = ""
        self._quantity = ""
        self._product_id = ""
        self._total = ""
        self._size = ""

    def Save(self):
        # save the object and return the id

        # new_id = db.seq.find_and_modify(query={'seq_name':'order_detail_seq'},update={'$inc': {'id': 1}},fields={'id': 1, '_id': 0},new=True,upsert=True)["id"]

        # object_id = self.collection.insert(
        #   {
        #   "id":new_id,
        #   "order_id":self.order_id,
        #   "quantity":self.quantity,
        #   "product_id":self.product_id,
        #   "total":self.total
        #   })

        # return str(object_id)

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''\
                insert into "Order_Detail" (order_id,
                                            quantity,
                                            product_id,
                                            subtotal,
                                            size,
                                            price) 
                values (%(order_id)s,
                        %(quantity)s,
                        %(product_id)s,
                        %(subtotal)s,
                        %(size)s,
                        %(price)s) 
                returning id'''

        parametros = {
            "order_id":self.order_id,
            "quantity":self.quantity,
            "product_id":self.product_id,
            "subtotal":float(self.subtotal),
            "size":self.size,
            "price": self.price
        }

        try:
            cur.execute(query, parametros)
            self.connection.commit()
            _id = cur.fetchone()[0]
            return _id
        except:
            return ""

    def ListByOrderId(self, order_id, page=1, limit=20):

        skip = (int(page) - 1) * int(limit)

        # order_detail = self.collection.find({"order_id":order_id}).skip(skip).limit(int(limit))

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = '''\
                    select od.*,
                           o.state,
                           p.name,
                           od.price,
                           p.color,
                           s.name as product_size,
                           p.sku,
                           s.id as size_id 
                    from "Order_Detail" od 
                    inner join "Product" p on od.product_id = p.id 
                    inner join "Product_Size" ps on ps.product_sku = p.sku
                    inner join "Size" s on s.id = ps.size_id
                    inner join "Order" o on od.order_id = o.id 
                    where od.order_id = %(order_id)s and s.name = od.size'''

            parameters = {
                "order_id": order_id,
                "limit": int(limit),
                "offset": skip
            }

            cur.execute(query, parameters)
            order_detail = cur.fetchall()
            return self.ShowSuccessMessage(order_detail)
        except Exception, e:
            return self.ShowError("No es posible obtener el detalle del pedido, {}".format(str(e)))

    def GetDetail(self, _id):

        # order_detail = self.collection.find_one({"id":_id})

        # return json_util.dumps(order_detail)

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            query = '''select * from "Order_Detail" where id = %(id)s limit 1'''
            parameters = {
                "id": _id
            }
            cur.execute(query, parameters)
            order_detail = cur.fetchone()
            return order_detail
        except:
            return {}
