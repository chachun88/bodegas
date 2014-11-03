#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
# from bson.objectid import ObjectId
from brand import Brand
from tag import Tag
from category import Category
import psycopg2
import psycopg2.extras
import re
import sys
from bson import json_util

class Product(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self._name = '' #nombre de producto
        self._sku = '' #id de producto
        self._description = '' #descripcion de producto
        self._brand = '' #marca de producto
        self._manufacturer = '' #proveedor
        self._size = [] #tallas
        self._color = [] #color
        self._material = '' #material
        self._bullet_1 = '' #viñeta 1
        self._bullet_2 = '' #viñeta 2
        self._bullet_3 = '' #viñeta 3
        self._currency = '' #divisa
        self._image = '' #imagen 1
        self._image_2 = '' #imagen 2
        self._image_3 = '' #imagen 3
        self._category = '' #categoria
        self._upc = '' #articulo
        self._price='' #precio compra
        self._sell_price = 0 #precio venta
        self._delivery = "" #texto delivery detalle de producto
        self._which_size = "" #texto cual es tu talla detalle de producto
        self._tags = ''

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
    

    def GetCellars(self):
        return ''

    def Print(self):
        try:
            rtn_data = {
                "id":self.id,
                "name":self.name,
                "description":self.description,
                "sku":self.sku,
                "brand":self.brand,
                "manufacturer":self.manufacturer,
                "size":self.size,
                "color":self.color,
                "material":self.material,
                "bullet_1":self.bullet_1,
                "bullet_2":self.bullet_2,
                "bullet_3":self.bullet_3,
                "image":self.image,
                "image_2":self.image_2,
                "image_3":self.image_3,
                # "currency":self.currency,
                "category":self.category,
                "upc":self.upc,
                "price":self.price,
                "tags":self.tags,
                "sell_price":self.sell_price,
                "which_size":self.which_size,
                "delivery":self.delivery
            }

            return rtn_data
        except Exception, e:
            return self.ShowError("id: " + self.id + " not found")

    def Save(self):
 
        # try:
        #   #if Category().Exist(self.category) == False and Brand().Exist(self.brand) == False:
        #   #   raise
        #   # print "coloooooooooooooooooor "+ self.color
        #   sizes=self.size.split(',')
        #   colors=self.color.split(',')
        #   if len(sizes) > len(colors):
        #       count=len(sizes)
        #   else:
        #       count=len(colors)

        #   sku_count = self.collection.find({"sku":self.sku}).count()

        #   ## solve when sku already exists
        #   if sku_count >= 1:
        #       for i in range(0,len(sizes)):
                    
        #           try:
        #               self.collection.update({
        #                       "sku":self.sku
        #                       },{
        #                       "$addToSet":{
        #                           "size":sizes[i]
        #                           }
        #                           })
        #           except Exception, e:
        #               print " except "+str(e)+ " i "  + str(i)
        #               pass
        #       for i in range(0,len(colors)):
                    
        #           try:
        #               self.collection.update({
        #                       "sku":self.sku
        #                       },{
        #                       "$addToSet":{
        #                           "color":colors[i]
        #                           }
        #                           })
        #           except Exception, e:
        #               print " except "+str(e)+ " i "  + str(i)
        #               pass            

        #       self.collection.update({
        #               "sku":self.sku
        #               },{
        #               "$set":{
        #                   "name":self.name,
        #                   "description":self.description,
        #                   "brand":self.brand,
        #                   "manufacturer":self.manufacturer,
        #                   # "size":self.sizes,
        #                   # "color":self.colors,
        #                   "material":self.material,
        #                   "bullet_1":self.bullet_1,
        #                   "bullet_2":self.bullet_2,
        #                   "bullet_3":self.bullet_3,
        #                   "image":self.image,
        #                   "image_2":self.image_2,
        #                   "image_3":self.image_3,
        #                   # "currency":self.currency,
        #                   "category":self.category,
        #                   "price":self.price,
        #                   "upc":self.upc
        #                   }
        #               })

        #       self.identifier = str(self.collection.find({"sku":self.sku})[0]["_id"])
        #   ##solve when id is not empty
        #   elif self.identifier.strip() != "":
        #       for i in range(0,len(sizes)):
                    
        #           try:
        #               self.collection.update({
        #                       "sku":self.sku
        #                       },{
        #                       "$addToSet":{
        #                           "size":sizes[i]
        #                           }
        #                           })
        #           except Exception, e:
        #               print " except "+str(e)+ " i "  + str(i)
        #               pass
        #       for i in range(0,len(colors)):
                    
        #           try:
        #               self.collection.update({
        #                       "sku":self.sku
        #                       },{
        #                       "$addToSet":{
        #                           "color":colors[i]
        #                           }
        #                           })
        #           except Exception, e:
        #               print " except "+str(e)+ " i "  + str(i)
        #               pass            


        #       self.collection.update({
        #               "_id":ObjectId(self.identifier)
        #           },{
        #           "$set":{
        #               "name":self.name,
        #               "description":self.description,
        #               "sku":self.sku,
        #               "brand":self.brand,
        #               "manufacturer":self.manufacturer,
        #               # "size":self.sizes,
        #               # "color":self.colors,
        #               "material":self.material,
        #               "bullet_1":self.bullet_1,
        #               "bullet_2":self.bullet_2,
        #               "bullet_3":self.bullet_3,
        #               "image":self.image,
        #               "image_2":self.image_2,
        #               "image_3":self.image_3,
        #               # "currency":self.currency,
        #               "category":self.category,
        #               "price":self.price,
        #               "upc":self.upc
        #           }})
                
        #   ##solve when the product does not exists
        #   else:
        #       self.identifier = str(self.collection.save({
        #               "name":self.name,
        #               "description":self.description,
        #               "sku":self.sku,
        #               "brand":self.brand,
        #               "manufacturer":self.manufacturer,
        #               # "size":self.size,
        #               # "color":self.color,
        #               "material":self.material,
        #               "bullet_1":self.bullet_1,
        #               "bullet_2":self.bullet_2,
        #               "bullet_3":self.bullet_3,
        #               "image":self.image,
        #               "image_2":self.image_2,
        #               "image_3":self.image_3,
        #               "category":self.category,
        #               "price":self.price,
        #               "upc":self.upc
        #           }))
                
        #       for i in range(count):
        #           self.collection.update({
        #                   "sku":self.sku
        #                   },{
        #                   "$addToSet":{
        #                       "size":sizes[i],
        #                       "color":colors[i]
        #                       }
        #                   })

        #   return self.ShowSuccessMessage("product correctly saved")
        # except Exception, e:
        #   return self.ShowError("product could not be saved")

        try:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            sizes=self.size.split(',')

            q = '''select count(*) as cantidad from "Product" where sku = %(sku)s'''
            p = {
            "sku":self.sku
            }

            sku_count = 0

            try:
                cur.execute(q,p)
                sku_count = cur.fetchone()["cantidad"]
            except Exception,e:
                return self.ShowError("Error checking if product exists, {}".format(str(e)))

            if sku_count >= 1:

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
                ,category_id = %(category_id)s 
                ,price = %(price)s 
                ,upc = %(upc)s
                ,color = %(color)s
                ,sell_price = %(sell_price)s
                ,which_size = %(which_size)s
                ,delivery = %(delivery)s where sku = %(sku)s returning id'''

                category = Category()
                category.name = self.category
                res = category.Save()

                if "error" in res:
                    return self.ShowError("Category can not be saved {}".format(res["error"]))

                p = {
                        "name":self.name,
                        "description":self.description,
                        "brand":self.brand,
                        "manufacturer":self.manufacturer,
                        "size":sizes,
                        "color":self.color,
                        "material":self.material,
                        "bullet_1":self.bullet_1,
                        "bullet_2":self.bullet_2,
                        "bullet_3":self.bullet_3,
                        "image":self.image,
                        "image_2":self.image_2,
                        "image_3":self.image_3,
                        "delivery":self.delivery,
                        "which_size":self.which_size,
                        # "currency":self.currency,
                        "category_id":category.id,
                        "price":self.price,
                        "upc":self.upc,
                        "sku":self.sku,
                        "sell_price":self.sell_price
                    }

                try:

                    # print "existe sku:{}".format(cur.mogrify(q,p))
                    cur.execute(q,p)

                    self.connection.commit()
                    self.id = cur.fetchone()["id"]

                    # print self.id

                except Exception,e:
                    return self.ShowError("Error updating product, {}".format(str(e)))

                q = '''update "Product" set size = (select ARRAY(select unnest(size) union select unnest(%(size)s))) where sku = %(sku)s'''

                p = {
                        "size":sizes,
                        "sku":self.sku
                    }

                try:
                    cur.execute(q,p)
                    self.connection.commit()

                except Exception,e:
                    return self.ShowError("Error updating product size, {}".format(str(e)))

                _tag = Tag()
                remover_asociacion = _tag.RemoveTagsAsociation(self.id)

                if "error" in remover_asociacion:
                    return self.ShowError(remover_asociacion["error"])

                # print "type:{} value:{}".format(type(self.tags.split(",")),self.tags.split(","))

                for t in self.tags.split(","):
                    res = _tag.AddTagProduct(t,self.id)
                    if "error" in res:
                        return self.ShowError(res["error"])

                return self.ShowSuccessMessage("product correctly updated by sku")

            elif self.id.strip() != "":

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
                , category_id = %(category_id)s 
                , price = %(price)s 
                , upc = %(upc)s
                , sku = %(sku)s
                , color = %(color)s
                , sell_price = %(sell_price)s
                , which_size = %(which_size)s
                , delivery = %(delivery)s where id = %(id)s'''

                category = Category()
                category.name = self.category
                res = category.Save()

                if "error" in res:
                    return self.ShowError("Category can not be saved {}".format(res["error"]))

                p = {
                        "name":self.name,
                        "description":self.description,
                        "brand":self.brand,
                        "manufacturer":self.manufacturer,
                        "size":sizes,
                        "color":self.color,
                        "material":self.material,
                        "bullet_1":self.bullet_1,
                        "bullet_2":self.bullet_2,
                        "bullet_3":self.bullet_3,
                        "image":self.image,
                        "image_2":self.image_2,
                        "image_3":self.image_3,
                        "sku":self.sku,
                        "category_id":category.id,
                        "price":self.price,
                        "upc":self.upc,
                        "id":self.id,
                        "sell_price":self.sell_price,
                        "delivery":self.delivery,
                        "which_size":self.which_size
                    }

                # print "existe id:{}".format(cur.mogrify(q,p))
                try:
                    cur.execute(q,p)
                    self.connection.commit()
                except Exception,e:
                    return self.ShowError("Error updating by id:{}".format(str(e)))

                q = '''update "Product" set size = (select ARRAY(select unnest(size) union select unnest(%(size)s))) where id = %(id)s'''

                p = {
                        "size":sizes,
                        "id":self.id
                    }

                try:
                    cur.execute(q,p)
                    self.connection.commit()

                except Exception,e:
                    return self.ShowError("Error updating product size, {}".format(str(e)))

                
                # self.id = cur.fetchone()[0]

                _tag = Tag()
                remover_asociacion = _tag.RemoveTagsAsociation(self.id)

                if "error" in remover_asociacion:
                    return self.ShowError(remover_asociacion["error"])

                # print self.tags

                for t in self.tags.split(","):
                    res = _tag.AddTagProduct(t.strip(),self.id)
                    if "error" in res:
                        return self.ShowError(res["error"])

                return self.ShowSuccessMessage("product correctly updated by id")

            elif self.sku != "":

                q = '''insert into "Product" (delivery,which_size,name,description,sku,brand,manufacturer,material,bullet_1,bullet_2,bullet_3,image,image_2,image_3, category_id, price, upc,size,color,sell_price)
                values (%(delivery)s,%(which_size)s,%(name)s,%(description)s,%(sku)s,%(brand)s,%(manufacturer)s,%(material)s,%(bullet_1)s,%(bullet_2)s,%(bullet_3)s,%(image)s,%(image_2)s,%(image_3)s,%(category_id)s,%(price)s,%(upc)s,%(size)s,%(color)s,%(sell_price)s) returning id'''

                category = Category()
                category.name = self.category
                res = category.Save()

                if "error" in res:
                    return self.ShowError("Category can not be saved {}".format(res["error"]))

                p = {
                        "name":self.name,
                        "description":self.description,
                        "sku":self.sku,
                        "brand":self.brand,
                        "manufacturer":self.manufacturer,
                        "size":sizes,
                        "color":self.color,
                        "material":self.material,
                        "bullet_1":self.bullet_1,
                        "bullet_2":self.bullet_2,
                        "bullet_3":self.bullet_3,
                        "image":self.image,
                        "image_2":self.image_2,
                        "image_3":self.image_3,
                        "category_id":category.id,
                        "price":self.price,
                        "upc":self.upc,
                        "sell_price":self.sell_price,
                        "delivery":self.delivery,
                        "which_size":self.which_size
                    }

                # print cur.mogrify(q.strip(),p)

                try:
                    cur.execute(q,p)
                    self.connection.commit()
                except Exception,e:
                    return self.ShowError("Error inserting new product: {} query: {}".format(str(e),cur.mogrify(q.strip(),p)))
                

                self.id = cur.fetchone()["id"]

                _tag = Tag()
                remover_asociacion = _tag.RemoveTagsAsociation(self.id)

                if "error" in remover_asociacion:
                    return self.ShowError(remover_asociacion["error"])

                print "type:{} value:{}".format(type(self.tags.split(",")),self.tags.split(","))

                for t in self.tags.split(","):
                    res = _tag.AddTagProduct(t.strip(),self.id)
                    if "error" in res:
                        return self.ShowError(res["error"])

                

                return self.ShowSuccessMessage("product correctly inserted")

            else:

                return self.ShowError("No viene sku")
            

        except Exception,e:
            return self.ShowError("product could not be saved, error:{}".format(str(e)))



    def InitBySku(self, sku):

        # data = self.collection.find({"sku":sku})

        # if data.count() >= 1:
        #   self.identifier = str(data[0]["_id"])
        #   self.name = data[0]["name"]
        #   self.description = data[0]["description"]
        #   self.brand = data[0]["brand"]
        #   self.manufacturer = data[0]["manufacturer"]
        #   self.size = data[0]["size"]
        #   self.color = data[0]["color"]
        #   self.material = data[0]["material"]
        #   self.bullet_1 = data[0]["bullet_1"]
        #   self.bullet_2 = data[0]["bullet_2"]
        #   self.bullet_3 = data[0]["bullet_3"]
        #   self.image = data[0]["image"]
        #   self.image_2 = data[0]["image_2"]
        #   self.image_3 = data[0]["image_3"]
        #   # self.currency=data[0]["currency"]
        #   self.category = data[0]["category"]
        #   self.upc = data[0]["upc"]
        #   self.sku = data[0]["sku"]
        #   self.price = data[0]["price"]

        #   return self.ShowSuccessMessage("product initialized")
        # return self.ShowError("product can not be initialized")



        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select p.*,c.name as category from "Product" p left join "Category" c on c.id = p.category_id where p.sku = %(sku)s limit 1'''
        p = {
        "sku":sku
        }
        try:

            # print cur.mogrify(q,p)

            cur.execute(q,p)
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
        except Exception,e:
            return self.ShowError("product cannot be initialized, {}".format(str(e)))
        

    def InitById(self, identifier):
        

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select p.*,c.name as category from "Product" p left join "Category" c on c.id = p.category_id where p.id = %(id)s limit 1'''
        p = {
        "id":identifier
        }
        try:
            cur.execute(q,p)
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
        except Exception,e:
            return self.ShowError("product cannot be initialized, error: {}".format(str(e)))

    def Exist(self, name):
        # if self.collection.find({"name":name}).count() >= 1:
        #   return True
        # return False

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        q = '''select * from "Product" where name = %(name)s limit 1'''
        p = {
        "name":name
        }
        try:
            cur.execute(q,p)
            product = cur.fetchone()

            if product:
                return True
            else:
                return False
        except:
            return False

    def Search(self, query):

        # if query == "":
        #   return []

        # regx = re.compile("^" + query, re.IGNORECASE)

        # data = self.collection.find({"name":regx}).limit(5)

        # return data
    
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        q = '''select p.*,c.name as category from "Product" p left join "Category" c on c.id = p.category_id where lower(p.name) like %(name)s limit 5'''
        p = {
        "name":"%{}%".format(query.lower())
        }
        print cur.mogrify(q,p)
        try:
            cur.execute(q,p)
            products = cur.fetchall()

            if cur.rowcount > 0:
                return products
            else:
                return {}
        except:
            return {}


    def GetList(self, page, items):

        page = int(page)
        items = int(items)
        offset = (page-1)*items
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            q = '''select p.*,c.name as category from "Product" p left join "Category" c on c.id = p.category_id order by p.sku limit %(items)s offset %(offset)s'''
            p = {
                "items":items,
                "offset":offset
                }
            cur.execute(q,p)
            lista = cur.fetchall()
            return lista
        except Exception,e:
            print str(e)
            return {}