#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
from kardex import Kardex
import model10
from model10.size import Size
from tag import Tag
from category import Category
import psycopg2
import psycopg2.extras
import datetime


class Product(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._name = ''  # nombre de producto
        self._sku = ''  # id de producto
        self._description = ''  # descripcion de producto
        self._brand = ''  # marca de producto
        self._manufacturer = ''  # proveedor
        self._size = []  # tallas
        self._color = []  # color
        self._material = ''  # material
        self._bullet_1 = ''  # viñeta 1
        self._bullet_2 = ''  # viñeta 2
        self._bullet_3 = ''  # viñeta 3
        self._currency = ''  # divisa
        self._image = ''  # imagen 1
        self._image_2 = ''  # imagen 2
        self._image_3 = ''  # imagen 3
        self._image_4 = ''  # imagen 4
        self._image_5 = ''  # imagen 5
        self._image_6 = ''  # imagen 6
        self._category = ''  # categoria
        self._upc = ''  # articulo
        self._price = ''  # precio compra
        self._sell_price = 0  # precio venta
        self._delivery = ""  # texto delivery detalle de producto
        self._which_size = ""  # texto cual es tu talla detalle de producto
        self._tags = ''
        self._promotion_price = 0  # precio promocion
        self._size_id = ""

        # self.collection = db.product

        self.table = 'Product'

    @property
    def upc(self):
        return self._upc

    @upc.setter
    def upc(self, value):
        self._upc = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, value):
        self._sku = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def manufacturer(self):
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value):
        self._manufacturer = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def size_id(self):
        return self._size_id

    @size_id.setter
    def size_id(self, value):
        self._size_id = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def material(self):
        return self._material

    @material.setter
    def material(self, value):
        self._material = value

    @property
    def bullet_1(self):
        return self._bullet_1

    @bullet_1.setter
    def bullet_1(self, value):
        self._bullet_1 = value

    @property
    def bullet_2(self):
        return self._bullet_2

    @bullet_2.setter
    def bullet_2(self, value):
        self._bullet_2 = value

    @property
    def bullet_3(self):
        return self._bullet_3

    @bullet_3.setter
    def bullet_3(self, value):
        self._bullet_3 = value

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._currency = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def image_2(self):
        return self._image_2

    @image_2.setter
    def image_2(self, value):
        self._image_2 = value

    @property
    def image_3(self):
        return self._image_3

    @image_3.setter
    def image_3(self, value):
        self._image_3 = value

    @property
    def image_4(self):
        return self._image_4

    @image_4.setter
    def image_4(self, value):
        self._image_4 = value

    @property
    def image_5(self):
        return self._image_5

    @image_5.setter
    def image_5(self, value):
        self._image_5 = value

    @property
    def image_6(self):
        return self._image_6

    @image_6.setter
    def image_6(self, value):
        self._image_6 = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

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
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def delivery(self):
        return self._delivery

    @delivery.setter
    def delivery(self, value):
        self._delivery = value

    @property
    def which_size(self):
        return self._which_size

    @which_size.setter
    def which_size(self, value):
        self._which_size = value

    @property
    def promotion_price(self):
        return self._promotion_price

    @promotion_price.setter
    def promotion_price(self, value):
        self._promotion_price = value

    def GetCellars(self):
        return ''

    def Print(self):
        try:
            rtn_data = {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "sku": self.sku,
                "brand": self.brand,
                "manufacturer": self.manufacturer,
                "size": self.size,
                "color": self.color,
                "material": self.material,
                "bullet_1": self.bullet_1,
                "bullet_2": self.bullet_2,
                "bullet_3": self.bullet_3,
                "image": self.image,
                "image_2": self.image_2,
                "image_3": self.image_3,
                "image_4": self.image_4,
                "image_5": self.image_5,
                "image_6": self.image_6,
                "promotion_price": self.promotion_price,
                "category": self.category,
                "upc": self.upc,
                "price": self.price,
                "tags": self.tags,
                "sell_price": self.sell_price,
                "which_size": self.which_size,
                "delivery": self.delivery,
                "size_id": self.size_id
            }

            return rtn_data
        except Exception, e:
            return self.ShowError("not found {}".format(str(e)))

    def Save(self):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        sizes = self.size.split(',')

        q = '''select count(*) as cantidad from "Product" where sku = %(sku)s'''
        p = {
            "sku": self.sku
        }

        sku_count = 0

        try:
            cur.execute(q, p)
            sku_count = cur.fetchone()["cantidad"]
        except Exception, e:
            return self.ShowError("Error checking if product exists, {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

        if sku_count > 0:

            q = '''update "Product" set 
            name = %(name)s 
            ,description = %(description)s 
            ,brand = %(brand)s 
            ,manufacturer = %(manufacturer)s 
            ,material = %(material)s 
            ,bullet_1 = %(bullet_1)s 
            ,bullet_2 = %(bullet_2)s 
            ,image = %(image)s 
            ,image_2 = %(image_2)s 
            ,image_3 = %(image_3)s 
            ,image_4 = %(image_4)s 
            ,image_5 = %(image_5)s 
            ,image_6 = %(image_6)s 
            ,category_id = %(category_id)s 
            ,price = %(price)s 
            ,upc = %(upc)s
            ,color = %(color)s
            ,sell_price = %(sell_price)s
            ,which_size = %(which_size)s
            ,promotion_price = %(promotion_price)s
            ,delivery = %(delivery)s where sku = %(sku)s returning id'''

            category = Category()
            category.name = self.category
            res = category.Save()

            if "error" in res:
                return self.ShowError("Category can not be saved {}".format(res["error"]))

            p = {
                "name": self.name,
                "description": self.description,
                "brand": self.brand,
                "manufacturer": self.manufacturer,
                "size": sizes,
                "color": self.color,
                "material": self.material,
                "bullet_1": self.bullet_1,
                "bullet_2": self.bullet_2,
                "bullet_3": self.bullet_3,
                "image": self.image,
                "image_2": self.image_2,
                "image_3": self.image_3,
                "image_4": self.image_4,
                "image_5": self.image_5,
                "image_6": self.image_6,
                "delivery": self.delivery,
                "which_size": self.which_size,
                "promotion_price": self.promotion_price,
                "category_id": category.id,
                "price": self.price,
                "upc": self.upc,
                "sku": self.sku,
                "sell_price": self.sell_price
            }

            cur = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            try:

                # print "existe sku:{}".format(cur.mogrify(q,p))
                cur.execute(q, p)

                self.connection.commit()
                self.id = cur.fetchone()["id"]

                # print self.id

            except Exception, e:
                return self.ShowError("Error updating product, {}".format(str(e)))
            finally:
                cur.close()
                self.connection.close()

            # sizes = [u'36.0',u'37.0']

            sizes_id = []

            for size in sizes:

                if size.strip() != "":
                    _size = Size()
                    _size.name = size
                    res_name = _size.initByName()

                    if "success" in res_name:
                        sizes_id.append(_size.id)

            for size_id in sizes_id:

                k = Kardex()
                res_stock = k.stockByProductSku(self.sku, size_id)

                if "success" in res_stock:

                    if res_stock["success"] == 0:

                        cellars = model10.cellar.Cellar.GetAllCellars()

                        for c in cellars:

                            kardex = Kardex()

                            kardex.product_sku = self.sku
                            kardex.cellar_identifier = c["id"]
                            kardex.operation_type = 'ingreso'
                            kardex.units = 0
                            kardex.price = self.price
                            kardex.sell_price = 0.0
                            kardex.size_id = size_id
                            kardex.color = self.color
                            kardex.total = 0.0
                            kardex.balance_units = 0
                            kardex.balance_price = 0.0
                            kardex.balance_total = 0.0
                            kardex.date = str(
                                datetime.datetime.now().isoformat())
                            kardex.user = "Sistema - Nueva talla"

                            kardex.Insert()

                else:
                    return res_stock

            cur = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            _tag = Tag()
            remover_asociacion = _tag.RemoveTagsAsociation(self.id)

            if "error" in remover_asociacion:
                return self.ShowError(remover_asociacion["error"])

            # print "type:{}
            # value:{}".format(type(self.tags.split(",")),self.tags.split(","))

            for t in self.tags.split(","):
                if t.strip() != "":
                    res = _tag.AddTagProduct(t.strip(), self.id)
                    if "error" in res:
                        return self.ShowError(res["error"])

            return self.ShowSuccessMessage("product correctly updated by sku")

        elif self.id.strip() != "":

            cur = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            q = '''update "Product" set 
            name=%(name)s 
            , description = %(description)s 
            , brand = %(brand)s 
            , manufacturer = %(manufacturer)s 
            , material = %(material)s 
            , bullet_1 = %(bullet_1)s 
            , bullet_2 = %(bullet_2)s 
            , image = %(image)s 
            , image_2 = %(image_2)s 
            , image_3 = %(image_3)s 
            , image_4 = %(image_4)s 
            , image_5 = %(image_5)s 
            , image_6 = %(image_6)s 
            , category_id = %(category_id)s 
            , price = %(price)s 
            , upc = %(upc)s
            , sku = %(sku)s
            , color = %(color)s
            , sell_price = %(sell_price)s
            , which_size = %(which_size)s
            , promotion_price = %(promotion_price)s
            , delivery = %(delivery)s where id = %(id)s'''

            category = Category()
            category.name = self.category
            res = category.Save()

            if "error" in res:
                return self.ShowError("Category can not be saved {}".format(res["error"]))

            p = {
                "name": self.name,
                "description": self.description,
                "brand": self.brand,
                "manufacturer": self.manufacturer,
                "size": sizes,
                "color": self.color,
                "material": self.material,
                "bullet_1": self.bullet_1,
                "bullet_2": self.bullet_2,
                "bullet_3": self.bullet_3,
                "image": self.image,
                "image_2": self.image_2,
                "image_3": self.image_3,
                "image_4": self.image_4,
                "image_5": self.image_5,
                "image_6": self.image_6,
                "sku": self.sku,
                "category_id": category.id,
                "price": self.price,
                "upc": self.upc,
                "id": self.id,
                "sell_price": self.sell_price,
                "delivery": self.delivery,
                "which_size": self.which_size,
                "promotion_price": self.promotion_price
            }

            # print "existe id:{}".format(cur.mogrify(q,p))
            try:
                cur.execute(q, p)
                self.connection.commit()
            except Exception, e:
                return self.ShowError("Error updating by id:{}".format(str(e)))
            finally:
                cur.close()
                self.connection.close()

            # sizes = [u'36.0',u'37.0']

            sizes_id = []

            for size in sizes:

                if size.strip() != "":
                    _size = Size()
                    _size.name = size
                    res_name = _size.initByName()

                    if "success" in res_name:
                        sizes_id.append(_size.id)

            for size_id in sizes_id:

                cur = self.connection.cursor(
                    cursor_factory=psycopg2.extras.RealDictCursor)

                query = '''select id from "Kardex" where product_sku = %(product_sku)s and size_id = %(size_id)s order by date desc limit 1'''

                parameter = {"product_sku": self.id, "size_id": size_id}

                try:
                    cur.execute(query, parameter)

                    if cur.rowcount == 0:

                        cellars = model10.cellar.Cellar.GetAllCellars()

                        for c in cellars:

                            kardex = Kardex()

                            kardex.product_sku = self.sku
                            kardex.cellar_identifier = c["id"]
                            kardex.operation_type = 'ingreso'
                            kardex.units = 0
                            kardex.price = self.price
                            kardex.sell_price = 0.0
                            kardex.size_id = size_id
                            kardex.color = self.color
                            kardex.total = 0.0
                            kardex.balance_units = 0
                            kardex.balance_price = 0.0
                            kardex.balance_total = 0.0
                            kardex.date = str(
                                datetime.datetime.now().isoformat())
                            kardex.user = "Sistema - Nueva talla"

                            kardex.Insert()

                except Exception, e:
                    return self.ShowError("2. Searching in kardex by size and product id, {}".format(str(e)))
                finally:
                    cur.close()
                    self.connection.close()

            _tag = Tag()
            remover_asociacion = _tag.RemoveTagsAsociation(self.id)

            if "error" in remover_asociacion:
                return self.ShowError(remover_asociacion["error"])

            # print self.tags

            # print "type:{}
            # value:{}".format(type(self.tags.split(",")),self.tags.split(","))

            for t in self.tags.split(","):
                if t.strip() != "":
                    res = _tag.AddTagProduct(t.strip(), self.id)
                    if "error" in res:
                        return self.ShowError(res["error"])

            return self.ShowSuccessMessage("product correctly updated by id")

        else:

            category = Category()
            category.name = self.category
            res = category.Save()

            if "error" in res:
                return self.ShowError("Category can not be saved {}".format(res["error"]))

            q = '''insert into "Product" (delivery,
                                        which_size,
                                        name,
                                        description,
                                        sku,
                                        brand,
                                        manufacturer,
                                        material,
                                        bullet_1,
                                        bullet_2,
                                        bullet_3,
                                        image,
                                        image_2,
                                        image_3,
                                        image_4,
                                        image_5,
                                        image_6,
                                        category_id,
                                        price,
                                        upc,
                                        color,
                                        sell_price,
                                        promotion_price)
            values (%(delivery)s,
                    %(which_size)s,
                    %(name)s,
                    %(description)s,
                    %(sku)s,
                    %(brand)s,
                    %(manufacturer)s,
                    %(material)s,
                    %(bullet_1)s,
                    %(bullet_2)s,
                    %(bullet_3)s,
                    %(image)s,
                    %(image_2)s,
                    %(image_3)s,
                    %(image_4)s,
                    %(image_5)s,
                    %(image_6)s,
                    %(category_id)s,
                    %(price)s,
                    %(upc)s,
                    %(color)s,
                    %(sell_price)s,
                    %(promotion_price)s) returning id'''

            p = {
                "name": self.name,
                "description": self.description,
                "sku": self.sku,
                "brand": self.brand,
                "manufacturer": self.manufacturer,
                "color": self.color,
                "material": self.material,
                "bullet_1": self.bullet_1,
                "bullet_2": self.bullet_2,
                "bullet_3": self.bullet_3,
                "image": self.image,
                "image_2": self.image_2,
                "image_3": self.image_3,
                "image_4": self.image_4,
                "image_5": self.image_5,
                "image_6": self.image_6,
                "category_id": category.id,
                "price": self.price,
                "upc": self.upc,
                "sell_price": self.sell_price,
                "delivery": self.delivery,
                "which_size": self.which_size,
                "promotion_price": self.promotion_price
            }

            # print cur.mogrify(q.strip(),p)

            cur = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            try:

                cur.execute(q, p)
                self.connection.commit()
                self.id = cur.fetchone()["id"]

                sizes_id = []

                for size in sizes:

                    if size.strip() != "":
                        _size = Size()
                        _size.name = size
                        res_name = _size.initByName()

                        if "success" in res_name:
                            sizes_id.append(_size.id)

                for size_id in sizes_id:

                    kardex = Kardex()
                    res_stock = kardex.stockByProductSku(self.sku, size_id)

                    if "success" in res_stock:

                        total = res_stock["success"]

                        if total == 0:

                            cellars = model10.cellar.Cellar.GetAllCellars()

                            for c in cellars:

                                kardex = Kardex()

                                kardex.product_sku = self.sku
                                kardex.cellar_identifier = c["id"]
                                kardex.operation_type = 'ingreso'
                                kardex.units = 0
                                kardex.price = self.price
                                kardex.sell_price = 0.0
                                kardex.size_id = size_id
                                kardex.color = self.color
                                kardex.total = 0.0
                                kardex.balance_units = 0
                                kardex.balance_price = 0.0
                                kardex.balance_total = 0.0
                                kardex.date = str(
                                    datetime.datetime.now().isoformat())
                                kardex.user = "Sistema - Nueva talla"

                                kardex.Insert()

                    else:
                        return self.ShowError("Getting stock by product sku, {}".format(res_stock["error"]))

                _tag = Tag()

                remover_asociacion = _tag.RemoveTagsAsociation(self.id)

                if "error" in remover_asociacion:
                    return self.ShowError(remover_asociacion["error"])

                # print "type:{} value:{}".format(type(self.tags),self.tags)

                for t in self.tags.split(","):
                    if t.strip() != "":
                        res = _tag.AddTagProduct(t.strip(), self.id)
                        if "error" in res:
                            return self.ShowError(res["error"])

                return self.ShowSuccessMessage("product correctly inserted")

            except Exception, e:
                return self.ShowError("Error inserting new product: {} query: {}".format(str(e), cur.mogrify(q.strip(), p)))
            finally:
                cur.close()
                self.connection.close()

    def InitBySku(self, sku):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select string_agg(s.name,',') as size, array_agg(s.size_id) as size_id, p.*, c.name as category from "Product" p 
                inner join "Category" c on c.id = p.category_id 
                inner join sizes s on s.product_sku = p.sku
                where p.sku = %(sku)s group by p.id, c.name limit 1'''
        p = {
            "sku": sku
        }
        try:

            # print cur.mogrify(q,p)

            cur.execute(q, p)
            producto = cur.fetchone()

            producto["tags"] = []

            tag = Tag()
            response = tag.GetTagsByProductId(producto["id"])

            if "success" in response:
                tags = response["success"]
                for t in tags:
                    producto["tags"].append(t["tag_id"])

            if cur.rowcount > 0:
                return self.ShowSuccessMessage(producto)
            else:
                return self.ShowError("product with sku {} not found".format(sku))
        except Exception, e:
            return self.ShowError("product cannot be initialized by sku, {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

    def InitById(self, identifier):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select string_agg(s.name,',') as size, array_agg(s.size_id) as size_id, p.*, c.name as category from "Product" p 
                inner join "Category" c on c.id = p.category_id 
                inner join sizes s on s.product_sku = p.sku
                where p.id = %(id)s group by p.id, c.name limit 1'''
        p = {
            "id": identifier
        }
        try:
            cur.execute(q, p)
            producto = cur.fetchone()

            # print producto

            producto["tags"] = []

            tag = Tag()
            response = tag.GetTagsByProductId(identifier)

            if "success" in response:
                tags = response["success"]
                for t in tags:
                    producto["tags"].append(t["tag_id"])

                # print producto

            # else:
            #   print response["error"]

            if cur.rowcount > 0:
                return self.ShowSuccessMessage(producto)
            else:
                return self.ShowError("product cannot be initialized")
        except Exception, e:
            return self.ShowError("product cannot be initialized, error: {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

    def Exist(self, name):
        # if self.collection.find({"name":name}).count() >= 1:
        #   return True
        # return False

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        q = '''select * from "Product" where name = %(name)s limit 1'''
        p = {
            "name": name
        }
        try:
            cur.execute(q, p)
            product = cur.fetchone()

            if product:
                return True
            else:
                return False
        except:
            return False
        finally:
            cur.close()
            self.connection.close()

    def Search(self, query):

        # if query == "":
        #   return []

        # regx = re.compile("^" + query, re.IGNORECASE)

        # data = self.collection.find({"name":regx}).limit(5)

        # return data

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        q = '''select p.*,c.name as category from "Product" p left join "Category" c on c.id = p.category_id where lower(p.name) like %(name)s limit 5'''
        p = {
            "name": "%{}%".format(query.lower())
        }
        print cur.mogrify(q, p)
        try:
            cur.execute(q, p)
            products = cur.fetchall()

            if cur.rowcount > 0:
                return products
            else:
                return {}
        except:
            return {}
        finally:
            cur.close()
            self.connection.close()

    def GetList(self, page, items):

        page = int(page)
        items = int(items)
        offset = (page - 1) * items

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            q = '''select string_agg(s.name,',') as size, p.*, c.name as category from "Product" p 
            inner join "Category" c on c.id = p.category_id 
            inner join sizes s on s.product_sku = p.sku
            group by p.id, c.name limit %(items)s offset %(offset)s'''
            p = {
                "items": items,
                "offset": offset
            }
            cur.execute(q, p)
            lista = cur.fetchall()
            return self.ShowSuccessMessage(lista)

        except Exception, e:
            return self.ShowError("getting list of products, {}".format(str(e)))

        finally:
            cur.close()
            self.connection.close()

    def ForSale(self, product_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        q = '''select for_sale from "Product" where id = %(id)s'''
        p = {
            "id": product_id
        }

        for_sale = 0

        try:
            cur.execute(q, p)
            for_sale = int(cur.fetchone()["for_sale"])
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            cur.close()
            self.connection.close()

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        q = '''update "Product" set for_sale = %(for_sale)s where id = %(id)s'''

        if for_sale == 0:
            p = {
                "id": product_id,
                "for_sale": 1
            }
            for_sale = 1
        else:
            p = {
                "id": product_id,
                "for_sale": 0
            }
            for_sale = 0

        try:
            cur.execute(q, p)
            self.connection.commit()
            return self.ShowSuccessMessage(for_sale)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            cur.close()
            self.connection.close()
