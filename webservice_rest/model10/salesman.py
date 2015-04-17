#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
from salesmanpermission import SalesmanPermission
# from bson.objectid import ObjectId
import psycopg2
import psycopg2.extras


class Salesman(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        # self.collection = db.salesman
        self.table = 'User'
        self._salesman_id = ''
        self._name = ''
        self._password = '' 
        self._email = ''
        self._permissions = []
        self._cellars = []
        self._permissions_name = []
        self._cellars_name = []
        self._lastname = ""

    @property
    def lastname(self):
        return self._lastname
    @lastname.setter
    def lastname(self, value):
        self._lastname = value
    

    @property
    def salesman_id(self):
        return self._salesman_id
    @salesman_id.setter
    def salesman_id(self, value):
        self._salesman_id = value
    

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        self._password = value

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        self._email = value

    @property
    def permissions(self):
        return self._permissions
    @permissions.setter
    def permissions(self, value):
        self._permissions = value

    @property
    def user_type(self):
        return self._user_type
    @user_type.setter
    def user_type(self, value):
        self._user_type = value
    
    @property
    def permissions_name(self):
        return self._permissions_name
    @permissions_name.setter
    def permissions_name(self, value):
        self._permissions_name = value

    @property
    def cellars(self):
        return self._cellars
    @cellars.setter
    def cellars(self, value):
        self._cellars = value

    @property
    def cellars_name(self):
        return self._cellars_name
    @cellars_name.setter
    def cellars_name(self, value):
        self._cellars_name = value
    
    
    

    def Print(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "permissions":self.permissions,
            "salesman_id":self.salesman_id,
            "permissions_name":self.permissions_name,
            "cellars":self.cellars,
            "cellars_name":self.cellars_name,
            "lastname":self.lastname
        }

    def Remove(self):
        try:
            #delete = self._permissions.RemoveAllByUser()
            #if "error" in delete:
            #   return delete

            return BaseModel.Remove(self)
        except Exception, e:
            return self.ShowError("error removing user")

    def Login(self, username, password):
        # data = self.collection.find({"email":username, "password":password})

        # if data.count() >= 1:
        #   self.InitByEmail(username) ## init user
        #   return True
        # return False

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        q = '''select count(1) from "User" where email = %(email)s and %(password)s limit 1'''
        p = {
        "email":username,
        "password":password
        }
        try:
            cur.execute(q,p)
            existe = cur.fetchone()
            if existe:
                return True
            else:
                return False
        except:
            return False

    def InitByEmail(self, email):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        q = '''\
            select  u.*, 
                    STRING_AGG(distinct p.name, ',') as permissions_name, 
                    STRING_AGG(distinct c.name, ',') as cellars_name from "User" u 
            inner join "Permission" p on p.id = any(u.permissions) 
            inner join "Cellar" c on c.id = any(u.cellar_permissions) 
            inner join "User_Types" ut on ut.id = u.type_id
            where u.email = %(email)s and ut.name = %(user_type)s
            group by u.id limit 1'''
        p = {
            "email":email,
            "user_type": 'Vendedor'
        }
        try:
            cur.execute(q,p)
            usuario = cur.fetchone()
            if cur.rowcount > 0:
                return self.ShowSuccessMessage(usuario)
            else:
                return self.ShowError("user : " + email + " not found")
        except:
            return self.ShowError("user : " + email + " not found")

    def InitById(self, idd):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        q = '''\
            select  u.*, 
                    STRING_AGG(distinct p.name, ',') as permissions_name, 
                    STRING_AGG(distinct c.name, ',') as cellars_name 
            from "User" u 
            inner join "Permission" p on p.id = any(u.permissions) 
            inner join "Cellar" c on c.id = any(u.cellar_permissions) 
            inner join "User_Types" ut on ut.id = u.type_id
            where u.id = %(id)s and ut.name = %(user_type)s
            group by u.id limit 1'''
        p = {
            "id":idd,
            "user_type": 'Vendedor'
        }
        try:
            cur.execute(q,p)
            usuario = cur.fetchone()
            return self.ShowSuccessMessage(usuario)
        except:
            return self.ShowError("user : " + idd + " not found")

    def GetPermissions(self):
        return self._permissions.FindPermissions(self.id)


    def AssignPermission(self, permission):
        ## TODO: validate if permission exist
        self._permissions.salesman_id   = self.id
        self._permissions.permission_id = permission
        return self._permissions.Save()


    def RemovePermission(self, permission):
        self._permissions.salesman_id = self.id
        self._permissions.permission_id = permission
        return self._permissions.RemovePermission()

    def Save(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select id from "Permission" where name = any(%(permissions)s)'''
        p = {
            "permissions":self.permissions
        }
        cur.execute(q,p)
        permisos = []

        for i in cur.fetchall():
            permisos.append(i["id"])

        q = '''select id from "Cellar" where name = any(%(cellars)s)'''
        p = {
            "cellars":self.cellars
        }
        cur.execute(q,p)
        bodegas = []

        for i in cur.fetchall():
            bodegas.append(i["id"])

        q = '''select id from "User_Types" where name = %(name)s'''
        p = {
            "name":"Vendedor"
        }
        cur.execute(q,p)
        tipo_usuario = cur.fetchone()["id"]

        q = '''select * from "User" where email = %(email)s limit 1'''
        p = {
            "email":self.email
        }
        cur.execute(q,p)
        usuario = cur.fetchone()

        try:

            if cur.rowcount > 0:
                self.id = usuario['id']
                q = '''update "User" set name = %(name)s, lastname = %(lastname)s, password = %(password)s, email = %(email)s, permissions = %(permissions)s, type_id = %(type_id)s, cellar_permissions = %(cellar_permissions)s where id = %(id)s'''
                p = {
                    "name":self.name,
                    "email":self.email,
                    "permissions":permisos,
                    "password":self.password,
                    "id":self.id,
                    "type_id":tipo_usuario,
                    "cellar_permissions":bodegas,
                    "lastname":self.lastname
                }
                cur.execute(q,p)
                self.connection.commit()
                return self.ShowSuccessMessage(str(self.id))
            else:
                q = '''insert into "User" (name,password,email,permissions,type_id,cellar_permissions,lastname) values (%(name)s,%(password)s,%(email)s,%(permissions)s,%(type_id)s,%(cellar_permissions)s,%(lastname)s) returning id'''
                p = {
                    "name":self.name,
                    "lastname":self.lastname,
                    "email":self.email,
                    "permissions":permisos,
                    "password":self.password,
                    "type_id":tipo_usuario,
                    "cellar_permissions":bodegas
                }
                cur.execute(q,p)
                self.connection.commit()
                self.id = cur.fetchone()["id"]

                return self.ShowSuccessMessage(str(self.id))
        except Exception,e:
            return self.ShowError("failed to save user {}, error:{}".format(self.email,str(e)))

    def GetList(self, page, items):

        page = int(page)
        items = int(items)
        offset = (page-1)*items
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            q = '''\
                select  u.*, 
                        STRING_AGG(distinct p.name, ',') as permissions_name, 
                        STRING_AGG(distinct c.name, ',') as cellars_name from "User" u 
                inner join "Permission" p on p.id = any(u.permissions) 
                inner join "Cellar" c on c.id = any(u.cellar_permissions) 
                inner join "User_Types" ut on ut.id = u.type_id
                where ut.name = %(user_type)s
                group by u.id limit %(limit)s offset %(offset)s'''
            p = {
                "limit":items,
                "offset":offset,
                "user_type": 'Vendedor'
            }
            cur.execute(q,p)

            lista = cur.fetchall()
            return lista
        except Exception,e:
            print str(e)
            return {}
