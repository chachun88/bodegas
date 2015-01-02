#!/usr/bin/python
# -*- coding: UTF-8 -*-

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib
import urllib2
import pprint

from basehandler import BaseHandler
from bson import json_util

from model.base_model import BaseModel

class Product(BaseModel):

#   def get_product_list(self):
#       return [{"name":"p1"},{"name":"p2"},{"name":"p3"}]

    def __init__(self):
        BaseModel.__init__(self)
        self._identifier=""
        self._category=""
        self._sku=""
        self._name=""
        self._upc=""        
        self._description=""
        self._brand=""
        self._manufacturer=""
        self._size=[]
        self._color=""
        self._material=""
        self._bullet_1=""
        self._bullet_2=""
        self._bullet_3=""
        self._currency=""
        self._price=""
        self._image=""
        self._image_2=""
        self._image_3=""
        self._image_4=""
        self._image_5=""
        self._image_6=""
        self._sell_price = 0
        self._tags = ""
        self._which_size = ""
        self._delivery = ""
        

    ####################
    ### Class fields ###
    ####################    

    @property
    def identifier(self):
        return self._identifier
    @identifier.setter
    def identifier(self, value):
        self._identifier = value    

    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, value):
        self._category = value      
    
    @property
    def sku(self):
        return self._sku
    @sku.setter
    def sku(self, value):
        self._sku = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def upc(self):
        return self._upc
    @upc.setter
    def upc(self, value):
        self._upc = value
    
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
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        self._price = value

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
    def for_sale(self):
        return self._for_sale
    @for_sale.setter
    def for_sale(self, value):
        self._for_sale = value
    
    
    #################
    #### Methods ####
    #################

    def InitWithId(self, idd):
        url = self.wsurl() + "/product/find"

        url += "?token=" + self.token
        url += "&id=" + idd

        json_string = urllib.urlopen(url).read()
        data_obj = json_util.loads(json_string)

        if "success" in data_obj:

            data = data_obj["success"]

            self.identifier = data["id"]
            self.category = data["category"]
            self.sku = data["sku"]
            self.name = data["name"] 
            self.upc= data["upc"]
            self.description = data["description"]
            self.brand = data["brand"]
            self.manufacturer= data["manufacturer"]
            self.size=data["size"]
            self.color= data["color"]
            self.material = data["material"] 
            self.bullet_1=data ["bullet_1"]
            self.bullet_2=data ["bullet_2"]
            self.bullet_3=data ["bullet_3"]
            # self.currency=data ["currency"]
            self.price =data["price"]
            self.image = data["image"]
            self.image_2 = data["image_2"]
            self.image_3 = data["image_3"]
            self.image_4 = data["image_4"]
            self.image_5 = data["image_5"]
            self.image_6 = data["image_6"]
            self.sell_price = data["sell_price"]
            self.tags = data["tags"]
            self.which_size = data["which_size"]
            self.delivery = data["delivery"]
            self.for_sale = data["for_sale"]

        return data_obj



    def InitWithSku(self, sku):
        url = self.wsurl() + "/product/find"

        url += "?token=" + self.token
        url += "&sku=" + sku

        json_string = urllib.urlopen(url).read()
        data = json_util.loads(json_string)

        if "success" in data:

            producto = data["success"]

            self.identifier = producto["id"]
            self.category = producto["category"]
            self.sku = producto["sku"]
            self.name = producto["name"] 
            self.upc= producto["upc"]
            self.description = producto["description"]
            self.brand = producto["brand"]
            self.manufacturer= producto["manufacturer"]
            self.size=producto["size"]
            self.color= producto["color"]
            self.material = producto ["material"] 
            self.bullet_1=producto ["bullet_1"]
            self.bullet_2=producto ["bullet_2"]
            self.bullet_3=producto ["bullet_3"]
            # self.currency=producto ["currency"]
            self.price=producto["price"]
            self.image = producto ["image"]
            self.image_2 = producto ["image_2"]
            self.image_3 = producto ["image_3"] 
            self.image_4 = producto ["image_4"]
            self.image_5 = producto ["image_5"]
            self.image_6 = producto ["image_6"]
            self.sell_price = producto["sell_price"]
            self.tags = producto["tags"]
            self.which_size = producto["which_size"]
            self.delivery = producto["delivery"]
            self.for_sale = producto["for_sale"]
        
        return data


    def Remove(self):
        if self.identifier!="":
            url=self.wsurl() + "/product/remove"
            url+="?token=" + self.token
            url+="&id={}".format(self.identifier)
            print urllib.urlopen(url).read()

    def Save(self, typee="other"):

        url = self.wsurl()+"/product/add?token=" + self.token

        if typee == "masive":          

            data = {
                "category" : self.category,
                "sku" : self.sku,
                "name" : self.name,
                "upc" : self.upc,
                "description" : self.description,
                "brand" : self.brand,
                "manufacturer" : self.manufacturer,
                "size" : self.size,
                "color" : self.color,
                "bullet_1" : self.bullet_1,
                "bullet_2" : self.bullet_2,
                "bullet_3" : self.bullet_3,
                "price" : self.price,
                "image" : self.image,
                "image_2" : self.image_2,
                "image_3" : self.image_3,
                "image_4" : self.image_4,
                "image_5" : self.image_5,
                "image_6" : self.image_6,
                "sell_price" : self.sell_price,
                "tags" : self.tags, # se envia como string
                "delivery" : self.delivery,
                "which_size" : self.which_size,
                "id" : self.identifier,
                "for_sale": self.for_sale
            }


            post_data = urllib.urlencode(data)

            response_str = urllib.urlopen(url, post_data).read()

            # print "masive:{}".format(response_str)

            return json_util.loads(response_str)

        else:   

            
            data = {
                "category" : self.category,
                "sku" : self.sku,
                "name" : self.name,
                "upc" : self.upc,
                "description" : self.description,
                "brand" : self.brand,
                "manufacturer" : self.manufacturer,
                "size" : self.size,
                "color" : self.color,
                "bullet_1" : self.bullet_1,
                "bullet_2" : self.bullet_2,
                "bullet_3" : self.bullet_3,
                "price" : self.price,
                "image" : self.image,
                "image_2" : self.image_2,
                "image_3" : self.image_3,
                "image_4" : self.image_4,
                "image_5" : self.image_5,
                "image_6" : self.image_6,
                "sell_price" : self.sell_price,
                "id" : self.identifier,
                "tags" : self.tags,
                "delivery" : self.delivery,
                "which_size" : self.which_size,
                "for_sale" : self.for_sale
            }

            post_data = urllib.urlencode(data)

            response_str = urllib.urlopen(url, post_data).read()

            print "one:{}".format(response_str)

            return json_util.loads(response_str)

    def get_product_list(self,items=100):
            
        url = self.wsurl()+"/product/list?token=" + self.token + "&items={}".format(items)
        content = urllib2.urlopen(url).read()

        # parse content to array data
        data = json_util.loads(content)

        self.identifier = data


        return data

    def Search(self, query):
        url = self.wsurl() + "/product/search?token=" + self.token
        url += "&q=" + query
        # return urllib.urlopen(url).read()

        content = urllib2.urlopen(url).read()

        data = json_util.loads(content)

        self.identifier = data
        
        return data

    def ForSale(self, product_id):

        url = self.wsurl() + "/product/for_sale?token=" + self.token

        data = {
        "product_id":product_id
        }

        post_data = urllib.urlencode(data)

        response_str = urllib.urlopen(url, post_data).read()

        # print "one:{}".format(response_str)

        return json_util.loads(response_str)

