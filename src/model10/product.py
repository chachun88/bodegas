#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
from size import Size
from tag import Tag
from category import Category
import psycopg2
import psycopg2.extras
from product_size import Product_Size
from order import Order
import math

class Product(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._name = ''  # nombre de producto
        self._sku = ''  # id de producto
        self._description = ''  # descripcion de producto
        self._brand = ''  # marca de producto
        self._manufacturer = ''  # proveedor
        self._size = []  # tallas
        self._color = ''  # color
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
        self._bulk_price = 0

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

    @property
    def bulk_price(self):
        return self._bulk_price

    @bulk_price.setter
    def bulk_price(self, value):
        self._bulk_price = value

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
                "size_id": self.size_id,
                "bulk_price" : self.bulk_price
            }

            return rtn_data
        except Exception, e:
            return self.ShowError("not found {}".format(str(e)))

    def Save(self, masive=False):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select * from "Product" where sku = %(sku)s and deleted = %(deleted)s'''
        p = {
            "sku": self.sku,
            "deleted": False
        }

        sku_count = 0

        try:
            cur.execute(q, p)
            sku_count = cur.rowcount
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
            ,bulk_price = %(bulk_price)s
            ,delivery = %(delivery)s where sku = %(sku)s and deleted = %(deleted)s returning id'''

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
                "sell_price": self.sell_price,
                "bulk_price" : self.bulk_price,
                "deleted": False
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

            for size in self.size:

                if size.strip() != "":
                    _size = Size()
                    _size.name = size.strip()
                    res_name = _size.initByName()

                    if "success" in res_name:
                        sizes_id.append(_size.id)

            for size_id in sizes_id:

                ps = Product_Size()
                ps.product_sku = self.sku
                ps.size_id = size_id

                if not masive:
                    res_remove = ps.removeNonExisting(sizes_id)

                    if "error" in res_remove:
                        return self.ShowError(res_remove["error"])

                res_ps = ps.save()

                if "error" in res_ps:
                    return self.ShowError(res_ps["error"])

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
            , bulk_price = %(bulk_price)s
            , delivery = %(delivery)s where id = %(id)s and deleted = %(deleted)s'''

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
                "promotion_price": self.promotion_price,
                "bulk_price" : self.bulk_price,
                "deleted": False
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

            for size in self.size:

                if size.strip() != "":
                    _size = Size()
                    _size.name = size.strip()
                    res_name = _size.initByName()

                    if "success" in res_name:
                        sizes_id.append(_size.id)

            for size_id in sizes_id:

                ps = Product_Size()
                ps.product_sku = self.sku
                ps.size_id = size_id

                if not masive:
                    res_remove = ps.removeNonExisting(sizes_id)

                    if "error" in res_remove:
                        return self.ShowError(res_remove["error"])

                res_ps = ps.save()

                if "error" in res_ps:
                    return self.ShowError(res_ps["error"])

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
                                        promotion_price,
                                        bulk_price,
                                        deleted)
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
                    %(promotion_price)s,
                    %(bulk_price)s,
                    %(deleted)s) returning id'''

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
                "promotion_price": self.promotion_price,
                "bulk_price" : self.bulk_price,
                "deleted": False
            }

            # print cur.mogrify(q.strip(),p)

            cur = self.connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

            try:

                cur.execute(q, p)
                self.connection.commit()
                self.id = cur.fetchone()["id"]

                sizes_id = []

                for size in self.size:

                    if size.strip() != "":
                        _size = Size()
                        _size.name = size.strip()
                        res_name = _size.initByName()

                        if "success" in res_name:
                            sizes_id.append(_size.id)

                for size_id in sizes_id:

                    ps = Product_Size()
                    ps.product_sku = self.sku
                    ps.size_id = size_id

                    if not masive:
                        res_remove = ps.removeNonExisting(sizes_id)

                        if "error" in res_remove:
                            return self.ShowError(res_remove["error"])

                    res_ps = ps.save()

                    if "error" in res_ps:
                        return self.ShowError(res_ps["error"])

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

        q = '''select string_agg(s.name,',') as size, 
                array_agg(s.id) as size_id, 
                p.*, 
                c.name as category
                from "Product" p 
                inner join "Category" c on c.id = p.category_id 
                inner join "Product_Size" ps on ps.product_sku = p.sku
                inner join "Size" s on s.id = ps.size_id
                where p.sku = %(sku)s and deleted = %(deleted)s group by p.id, c.name limit 1'''
        p = {
            "sku": sku,
            "deleted": False
        }
        try:

            # print cur.mogrify(q,p)

            cur.execute(q, p)
            producto = cur.fetchone()

            producto["tags"] = []

            self.identifier = producto["id"]
            self.category = producto["category"]
            self.sku = producto["sku"]
            self.name = producto["name"]
            self.upc = producto["upc"]
            self.description = producto["description"]
            self.brand = producto["brand"]
            self.manufacturer = producto["manufacturer"]
            self.size = producto["size"].split(",")
            self.color = producto["color"]
            self.material = producto["material"]
            self.bullet_1 = producto["bullet_1"]
            self.bullet_2 = producto["bullet_2"]
            self.bullet_3 = producto["bullet_3"]
            self.size_id = producto["size_id"]
            self.price = producto["price"]
            self.image = producto["image"]
            self.image_2 = producto["image_2"]
            self.image_3 = producto["image_3"]
            self.image_4 = producto["image_4"]
            self.image_5 = producto["image_5"]
            self.image_6 = producto["image_6"]
            self.sell_price = producto["sell_price"]
            self.tags = producto["tags"]
            self.which_size = producto["which_size"]
            self.delivery = producto["delivery"]
            self.for_sale = producto["for_sale"]
            self.promotion_price = producto["promotion_price"]
            self.bulk_price = producto["bulk_price"]

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
            return self.ShowError("product cannot be initialized by sku {}, {}".format(sku, str(e)))
        finally:
            cur.close()
            self.connection.close()

    def InitById(self, identifier):

        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select string_agg(s.name,',') as size, array_agg(s.id) as size_id, p.*, c.name as category from "Product" p 
                inner join "Category" c on c.id = p.category_id 
                inner join "Product_Size" ps on ps.product_sku = p.sku
                inner join "Size" s on s.id = ps.size_id
                where p.id = %(id)s and deleted = %(deleted)s group by p.id, c.name limit 1'''
        p = {
            "id": identifier,
            "deleted": False
        }
        try:
            cur.execute(q, p)
            producto = cur.fetchone()
            producto["tags"] = []

            tag = Tag()
            response = tag.GetTagsByProductId(identifier)

            if "success" in response:
                tags = response["success"]
                for t in tags:
                    producto["tags"].append(t["tag_id"])

            if cur.rowcount > 0:
                self.id = producto["id"]
                self.category = producto["category"]
                self.sku = producto["sku"]
                self.name = producto["name"]
                self.upc = producto["upc"]
                self.description = producto["description"]
                self.brand = producto["brand"]
                self.manufacturer = producto["manufacturer"]
                self.size = producto["size"].split(",")
                self.color = producto["color"]
                self.material = producto["material"]
                self.bullet_1 = producto["bullet_1"]
                self.bullet_2 = producto["bullet_2"]
                self.bullet_3 = producto["bullet_3"]
                self.size_id = producto["size_id"]
                self.price = producto["price"]
                self.image = producto["image"]
                self.image_2 = producto["image_2"]
                self.image_3 = producto["image_3"]
                self.image_4 = producto["image_4"]
                self.image_5 = producto["image_5"]
                self.image_6 = producto["image_6"]
                self.sell_price = producto["sell_price"]
                self.tags = producto["tags"]
                self.which_size = producto["which_size"]
                self.delivery = producto["delivery"]
                self.for_sale = producto["for_sale"]
                self.promotion_price = producto["promotion_price"]
                self.bulk_price = producto["bulk_price"]
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

        q = '''select * from "Product" where name = %(name)s and deleted = %(deleted)s limit 1'''
        p = {
            "name": name,
            "deleted": False
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

        # q = '''select p.*,c.name as category from "Product" p 
        # left join "Category" c on c.id = p.category_id 
        # where lower(p.name) like %(name)s and deleted = %(deleted)s limit 5'''

        q = '''select string_agg(s.name,',') as size, p.*, c.name as category from "Product" p 
            inner join "Category" c on c.id = p.category_id 
            inner join "Product_Size" ps on ps.product_sku = p.sku
            inner join "Size" s on s.id = ps.size_id
            where p.deleted = %(deleted)s
            and lower(p.name) like %(name)s
            group by p.id, c.name 
            order by p.sku asc'''

        p = {
            "name": "%{}%".format(query.lower()),
            "deleted": False
        }

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

    def GetList(self, page = 1, items = 30, query = "", column = "p.name", direction = "asc", term=''):



        page = int(page)
        items = int(items)
        offset = (page - 1) * items

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            if page == 0 and items == 0:
                q = '''\
                select string_agg(s.name,',') as size, 
                p.*, 
                c.name as category from "Product" p 
                inner join "Category" c on c.id = p.category_id 
                inner join "Product_Size" ps on ps.product_sku = p.sku
                inner join "Size" s on s.id = ps.size_id
                where p.deleted = %(deleted)s
                {query}
                group by p.id, c.name 
                order by {column} {direction}'''.format(column=column, 
                                                        direction=direction, 
                                                        query=query)
                p = {
                    "deleted": False,
                    "term": term
                }
            else:
                q = '''\
                select string_agg(s.name,',') as size, 
                p.*, 
                c.name as category from "Product" p 
                inner join "Category" c on c.id = p.category_id 
                inner join "Product_Size" ps on ps.product_sku = p.sku
                inner join "Size" s on s.id = ps.size_id
                where p.deleted = %(deleted)s
                {query}
                group by p.id, c.name 
                order by {column} {direction}
                limit %(items)s offset %(offset)s'''.format(column=column, 
                                                            direction=direction, 
                                                            query=query)
                p = {
                    "items": items,
                    "offset": offset,
                    "deleted": False,
                    "term": term
                }
            # print cur.mogrify(q, p)
            cur.execute(q, p)
            lista = cur.fetchall()
            return self.ShowSuccessMessage(lista)

        except Exception, e:
            return self.ShowError("getting list of products, {}".format(str(e)))

        finally:
            cur.close()
            self.connection.close()

    def GetListTotalPages(self, items=30):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            q = '''select p.id from "Product" p 
            inner join "Category" c on c.id = p.category_id 
            inner join "Product_Size" ps on ps.product_sku = p.sku
            inner join "Size" s on s.id = ps.size_id
            where p.deleted = %(deleted)s
            group by p.id, c.name'''

            p = {
                "deleted": False
            }

            cur.execute(q, p)
            total_items = float(cur.rowcount)
            items = float(items)
            total_page = math.ceil(total_items/items)
            return self.ShowSuccessMessage(total_page)

        except Exception, e:
            return self.ShowError("getting total pages of list of products, {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

    def getTotalItems(self, query='', term=''):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''\
            select count(1) as items from "Product" p 
            inner join "Category" c on c.id = p.category_id 
            inner join "Product_Size" ps on ps.product_sku = p.sku
            inner join "Size" s on s.id = ps.size_id
            where p.deleted = %(deleted)s
            {query}
            group by p.id, c.name'''.format(query=query)

        p = {
            "deleted": False,
            "term": term
        }

        try:
            cur.execute(q, p)
            items = len(cur.fetchall())
            return self.ShowSuccessMessage(items)
        except Exception, e:
            return self.ShowError(str(e))
        finally:
            self.connection.close()
            cur.close()

    def ForSale(self, product_id):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        q = '''select for_sale from "Product" where id = %(id)s and deleted = %(deleted)s'''
        p = {
            "id": product_id,
            "deleted": False
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
        q = '''update "Product" set for_sale = %(for_sale)s where id = %(id)s and deleted = %(deleted)s'''

        if for_sale == 0:
            p = {
                "id": product_id,
                "for_sale": 1,
                "deleted": False
            }
            for_sale = 1
        else:
            p = {
                "id": product_id,
                "for_sale": 0,
                "deleted": False
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

    def Remove(self):

        try:

            if self.id != "":

                cur = self.connection.cursor()
                
                q = '''update "Product" set deleted = %(deleted)s where id = %(id)s'''
                p = {
                    "id":self.id,
                    "deleted": True
                }
                cur.execute(q,p)
                self.connection.commit()
                return self.ShowSuccessMessage("object: {} has been deleted".format(self.id))
            else:
                return self.ShowError("identifier not found")   
        except Exception, e:
            return self.ShowError("object: not found, error:{}".format(str(e)))

    def GetSizes(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''\
                select s.id, s.name from "Size" s
                inner join "Product_Size" ps on ps.size_id = s.id
                inner join "Product" p on p.sku = ps.product_sku
                where ps.product_sku = %(product_sku)s and p.deleted = %(deleted)s'''
        parameters = {
            "product_sku": self.sku,
            "deleted": False
        }

        try:
            cur.execute(query, parameters)
            sizes = cur.fetchall()
            self.connection.commit()
            return self.ShowSuccessMessage(sizes)
        except Exception, e:
            return self.ShowError("Get sizes by product sku, {}".format(str(e)))
        finally:
            cur.close()
            self.connection.commit()

    def getIdBySku(self, sku):

        product_id = None

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = '''
                select id from "Product"
                where sku = %(sku)s
                '''
        parameters = {
            "sku": sku
        }

        try:
            cursor.execute(query, parameters)
            product_id = cursor.fetchone()['id']
            self.connection.commit()
        except Exception, e:
            print str(e)
        finally:
            cursor.close()

        return product_id

    def reserved(self, sku, size):

        product = Product()
        product_id = product.getIdBySku(sku)

        total = 0

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''
                select sum(quantity) as total from "Order_Detail" od
                inner join "Order" o
                on o.id = od.order_id
                where od.product_id = %(product_id)s and od.size = %(size)s
                and ((o.state = %(pending)s and o.payment_type = %(payment_type)s) 
                   or o.state = %(confirmed)s or o.state = %(to_shipping)s)
                group by od.product_id
                '''
        parameters = {
            "product_id": product_id,
            "size": size,
            "pending": Order.ESTADO_PENDIENTE,
            "payment_type": 1,
            "confirmed": Order.ESTADO_CONFIRMADO,
            "to_shipping": Order.ESTADO_PARA_DESPACHO
        }

        try:
            cursor.execute(query, parameters)
            res = cursor.fetchone()
            total = res['total']
        except Exception, e:
            print str(e)
        finally:
            cursor.close()
            self.connection.close()

        return total
