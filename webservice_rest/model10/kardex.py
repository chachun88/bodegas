#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
# from cellar import Cellar
import psycopg2
import psycopg2.extras
import datetime

class Kardex(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._product_id = ''
        self._cellar_identifier = ''
        self._operation_type = Kardex.OPERATION_BUY
        self._units = 0
        self._price = 0.0
        self._sell_price = 0.0
        self._size= ''
        self._color=''
        self._total = 0.0
        self._balance_units = 0
        self._balance_price = 0.0
        self._balance_total = 0.0
        self._date = 0000000 
        self._user = ""

    OPERATION_BUY = "buy"
    OPERATION_SELL= "sell"
    OPERATION_MOV_IN = "mov_in"
    OPERATION_MOV_OUT = "mov_out"

    @property
    def user(self):
        return self._user
    @user.setter
    def user(self, value):
        self._user = value
    

    @property
    def product_id(self):
        return self._product_id
    @product_id.setter
    def product_id(self, value):
        self._product_id = value

    @property
    def cellar_identifier(self):
        return self._cellar_identifier
    @cellar_identifier.setter
    def cellar_identifier(self, value):
        self._cellar_identifier = value

    @property
    def operation_type(self):
        return self._operation_type
    @operation_type.setter
    def operation_type(self, value):
        self._operation_type = value

    @property
    def units(self):
        return self._units
    @units.setter
    def units(self, value):
        self._units = value

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        self._price = value

    @property
    def sell_price(self):
        return self._sell_price
    @sell_price.setter
    def sell_price(self, value):
        self._sell_price = value
        

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        self._size = value
    
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self._color = value

    @property
    def total(self):
        return self._total
    @total.setter
    def total(self, value):
        self._total = value

    @property
    def balance_units(self):
        return self._balance_units
    @balance_units.setter
    def balance_units(self, value):
        self._balance_units = value

    @property
    def balance_price(self):
        return self._balance_price
    @balance_price.setter
    def balance_price(self, value):
        self._balance_price = value

    @property
    def balance_total(self):
        return self._balance_total
    @balance_total.setter
    def balance_total(self, value):
        self._balance_total = value

    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, value):
        self._date = value

    def Save(self):
        return ''

    def InitById(self, idd):
        return ''
        
    def FindKardex(self, product_id, cellar_identifier,size):


        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Kardex" where product_id = %(product_id)s and cellar_id = %(cellar_id)s and size = %(size)s order by date desc limit 1'''

        parametros = {
        "product_id":product_id,
        "cellar_id":cellar_identifier,
        "size":size
        }

        try:
            cur.execute(query,parametros)
            kardex = cur.fetchone()

            self.id = kardex["id"]
            self.product_id = kardex["product_id"]
            self.operation_type = kardex["operation_type"]
            self.units = kardex["units"]
            self.price = kardex["price"]
            self.sell_price = kardex["sell_price"]
            self.size =kardex["size"]
            self.color = kardex["color"]
            self.total = kardex["total"]
            self.balance_units = kardex["balance_units"]
            self.balance_price = kardex["balance_price"]
            self.balance_total = kardex["balance_total"]
            self.date = kardex["date"]
            self.user = kardex["user"]
            self.cellar_identifier = kardex["cellar_id"]

            return self.ShowSuccessMessage("ok")

        except Exception,e:
            return self.ShowError(str(e))


    #take care of an infinite loop
    # return last kardex in the database
    def GetPrevKardex(self):


        new_kardex = Kardex()



        try:
            new_kardex.product_id = self.product_id
            new_kardex.cellar_identifier = self.cellar_identifier

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            query = '''select * from "Kardex" where product_id = %(product_id)s and cellar_id = %(cellar_id)s and size = %(size)s order by id desc limit 1'''

            parametros = {
            "product_id":self.product_id,
            "cellar_id":self.cellar_identifier,
            "size":self.size
            }
            cur.execute(query,parametros)
            # print "QUERY:{}".format(cur.query)
            kardex = cur.fetchone()

            if cur.rowcount > 0:
                new_kardex.id = kardex["id"]
                new_kardex.operation_type = kardex["operation_type"]
                new_kardex.units = kardex["units"]
                new_kardex.price = kardex["price"]
                new_kardex.sell_price = kardex["sell_price"]
                new_kardex.size =kardex["size"]
                new_kardex.color = kardex["color"]
                new_kardex.total = kardex["total"]
                new_kardex.balance_units = kardex["balance_units"]
                new_kardex.balance_price = kardex["balance_price"]
                new_kardex.balance_total = kardex["balance_total"]
                new_kardex.date = kardex["date"]
                new_kardex.user = kardex["user"]
                new_kardex.cellar_identifier = kardex["cellar_id"]
        except Exception, e:
            return self.ShowError("kardex not found, {}".format(str(e)))

        return self.ShowSuccessMessage(new_kardex)

    def Insert(self):

        response_prevkardex = self.GetPrevKardex()

        prev_kardex = Kardex()

        if "success" in response_prevkardex:
            prev_kardex = response_prevkardex["success"]
        else:
            return self.ShowError("error al obtener kardex, {}".format(response_prevkardex["error"]))

        ##parsing all to float
        self.price = float(self.price)
        self.total = float(self.total)
        self.balance_price = float(self.balance_price)
        self.balance_total = float(self.balance_total)
        self.units = int(self.units)

        ## doing maths...
        if self.operation_type == Kardex.OPERATION_SELL or self.operation_type == Kardex.OPERATION_MOV_OUT:
            self.price = prev_kardex.balance_price ## calculate price
        if self.price == "0":
            self.price = prev_kardex.balance_price

        self.total = self.units * self.price

        if self.operation_type == Kardex.OPERATION_BUY or self.operation_type == Kardex.OPERATION_MOV_IN:
            self.sell_price = "0"
            self.balance_units = prev_kardex.balance_units + self.units
            self.balance_total = prev_kardex.balance_total + self.total
        else:
            self.balance_units = prev_kardex.balance_units - self.units
            self.balance_total = prev_kardex.balance_total - self.total
 
        if self.balance_units != 0: ## prevent division by zero 
            self.balance_price = self.balance_total / self.balance_units

        ## truncate
        self.price = float(int(self.price * 100)) / 100.0
        self.total = round(float(int(self.total * 100)) / 100.0)
        self.balance_price = float(int(self.balance_price * 100)) / 100.0
        self.balance_total = round(float(int(self.balance_total * 100)) / 100.0)


        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        parametros = {
        "product_id":self.product_id,
        "cellar_id":self.cellar_identifier,
        "operation_type":self.operation_type,
        "units":self.units,
        "price":self.price,
        "sell_price":self.sell_price,
        "size":self.size,
        "color":self.color,
        "total":self.total,
        "balance_units":self.balance_units,
        "balance_price":self.balance_price,
        "balance_total":self.balance_total,
        "date":self.date,
        "user":self.user
        }

        try:
            query = '''insert into "Kardex" (balance_total,product_id,cellar_id,operation_type,units,price,sell_price,size,color,total,balance_units,balance_price,date,"user") values (%(balance_total)s,%(product_id)s,%(cellar_id)s,%(operation_type)s,%(units)s,%(price)s,%(sell_price)s,%(size)s,%(color)s,%(total)s,%(balance_units)s,%(balance_price)s,%(date)s,%(user)s)'''
            cur.execute(query,parametros)
            # return cur.mogrify(query,parametros)
            self.connection.commit()
            return self.ShowSuccessMessage("products has been added")
        except Exception,e:
            return self.ShowError("an error inserting kardex, error:{}".format(str(e)))

    def moveOrder(self, details, web_cellar, cellar_id):

        errors = []

        for d in details:

            kardex = Kardex()
            kardex.product_id = d["sku"]
            kardex.cellar_identifier = cellar_id
            kardex.date = str(datetime.datetime.now().isoformat())

            kardex.operation_type = Kardex.OPERATION_MOV_OUT
            kardex.units = d['quantity']
            kardex.price = d['price']
            kardex.size = d['size']

            kardex.color= d["color"]
            kardex.user = "Sistema"

            res_kardex = kardex.Insert()

            if "success" in res_kardex:

                kardex.cellar_identifier = web_cellar
                kardex.operation_type = Kardex.OPERATION_MOV_IN

                res_kardex_2 = kardex.Insert()

                if "error" in res_kardex_2:
                    errors.append(res_kardex_2["error"])
                    
            else:
                errors.append(res_kardex["error"])

        # end for

        if len(errors) > 0:
            return self.ShowError(errors)
        else:
            return self.ShowSuccessMessage("ok")

    ## only for debugging.
    def Debug(self, product_id, cellar_identifier, size):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select * from "Kardex" where product_id = %(product_id)s and cellar_id = %(cellar_id)s and size = %(size)s order by id desc limit 1'''

        parameters = {
        "product_id":product_id,
        "cellar_id":cellar_identifier,
        "size":size
        }

        # data = self.collection.find({
        #                   "product_id":self.product_id,
        #                   "cellar_identifier":self.cellar_identifier
        #                   }).sort("_id",1)

        try:
            cur.execute(query,parameters)
            data = cur.fetchone()

            for d in data:
                print d["operation_type"]
                print " units :     {}".format(d["units"])
                print " price :     {}".format(d["price"])
                print " sell_price :    {}".format(d["sell_price"])
                print " size :  {}".format(d["size"])
                print " color :     {}".format(d["color"])
                print " total :     {}".format(d["total"])
                print " balance units :     {}".format(d["balance_units"])
                print " balance price :     {}".format(d["balance_price"])
                print " balance total :     {}".format(d["balance_total"])

        except Exception,e:
            print str(e)
            pass

    def stockByProductId(self, product_id, size_id):

        """
        obtiene stock de producto por id, de todas las bodegas

        @param string product_id id de producto
        @param integer size id talla
        @return json si es exitoso retorna json con sucess de lo contrario retorna error
        """


        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        query = '''select sum(balance_units) from 
                (select distinct on(cellar_id) cellar_id, balance_units from "Kardex" 
                    where product_id = %(product_id)s 
                    and size_id = %(size_id)s 
                    order by cellar_id, date desc) 
                as kardex'''

        parametros = {
        "product_id":product_id,
        "size_id":size_id
        }

        try:
            cur.execute(query,parametros)
            kardex = cur.fetchone()

            self.id = kardex["id"]
            self.product_id = kardex["product_id"]
            self.operation_type = kardex["operation_type"]
            self.units = kardex["units"]
            self.price = kardex["price"]
            self.sell_price = kardex["sell_price"]
            self.size =kardex["size"]
            self.color = kardex["color"]
            self.total = kardex["total"]
            self.balance_units = kardex["balance_units"]
            self.balance_price = kardex["balance_price"]
            self.balance_total = kardex["balance_total"]
            self.date = kardex["date"]
            self.user = kardex["user"]
            self.cellar_identifier = kardex["cellar_id"]

            return self.ShowSuccessMessage("ok")

        except Exception,e:
            return self.ShowError(str(e))

