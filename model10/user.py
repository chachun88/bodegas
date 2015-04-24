#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel
import psycopg2
import psycopg2.extras


class UserType():
    GESTION = 1
    BODEGA = 6
    ADMINISTRADOR = 2


class Permission():

    API = 1
    NEW_PROD = 2
    SELL = 3
    MOD_CELLAR = 4
    ADM_USER = 5
    REPORT = 6


class User(BaseModel):
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
        self._type_id = ''

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

    @property
    def type_id(self):
        return self._type_id

    @type_id.setter
    def type_id(self, value):
        self._type_id = value

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
            return BaseModel.Remove(self)
        except Exception, e:
            return self.ShowError("error removing user {}".format(str(e)))

    def Login(self, username, password):
        # data = self.collection.find({"email":username, "password":password})

        # if data.count() >= 1:
        #   self.InitByEmail(username) ## init user
        #   return True
        # return False

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        q = '''\
            select count(1) from "User" u 
            inner join "User_Types" ut on ut.id = u.type_id
            where u.email = %(email)s and %(password)s and ut.id = any(%(user_type)s)
            limit 1'''
        p = {
            "email":username,
            "password":password,
            "user_type": [UserType.ADMINISTRADOR, UserType.GESTION, UserType.BODEGA]
        }
        try:
            cur.execute(q,p)
            existe = cur.fetchall()
            if existe.rowcount > 0:
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
                    STRING_AGG(distinct c.name, ',') as cellars_name,
                    ut.name as type,
                    ut.id as type_id
            from "User" u 
            inner join "Permission" p on p.id = any(u.permissions) 
            inner join "Cellar" c on c.id = any(u.cellar_permissions) 
            inner join "User_Types" ut on ut.id = u.type_id
            where u.email = %(email)s and ut.id = any(%(user_type)s)
            group by u.id, ut.name, ut.id limit 1'''
        p = {
            "email":email,
            "user_type": [UserType.ADMINISTRADOR, UserType.GESTION, UserType.BODEGA]
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
                    STRING_AGG(distinct c.name, ',') as cellars_name,
                    ut.name as type,
                    ut.id as type_id 
            from "User" u 
            inner join "Permission" p on p.id = any(u.permissions) 
            inner join "Cellar" c on c.id = any(u.cellar_permissions) 
            inner join "User_Types" ut on ut.id = u.type_id
            where u.id = %(id)s and ut.id = any(%(user_type)s)
            group by u.id, ut.name, ut.id limit 1'''
        p = {
            "id":idd,
            "user_type": [UserType.ADMINISTRADOR, UserType.GESTION, UserType.BODEGA]
        }
        try:
            cur.execute(q,p)
            usuario = cur.fetchone()
            return self.ShowSuccessMessage(usuario)
        except:
            return self.ShowError("user : " + idd + " not found")

    def Save(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select id from "Cellar" where name = any(%(cellars)s)'''
        p = {
            "cellars":self.cellars
        }
        cur.execute(q,p)
        bodegas = []

        for i in cur.fetchall():
            bodegas.append(i["id"])

        q = '''select * from "User" where email = %(email)s limit 1'''
        p = {
            "email":self.email
        }
        cur.execute(q,p)
        usuario = cur.fetchone()

        permisos = []

        try:

            if self.type_id == '':
                return self.ShowError("Debe seleccionar tipo de usuario")

            if UserType.ADMINISTRADOR == int(self.type_id):
                permisos = [
                            Permission.ADM_USER, 
                            Permission.API, 
                            Permission.MOD_CELLAR, 
                            Permission.SELL, 
                            Permission.NEW_PROD,
                            Permission.REPORT
                           ]
            elif UserType.BODEGA == int(self.type_id):
                permisos = [
                            Permission.MOD_CELLAR
                           ]
            elif UserType.GESTION == int(self.type_id):
                permisos = [
                            Permission.ADM_USER, 
                            Permission.MOD_CELLAR, 
                            Permission.SELL, 
                            Permission.REPORT
                           ]

            print permisos
            if cur.rowcount > 0:

                self.id = usuario['id']

                q = '''update "User" set name = %(name)s,
                                         lastname = %(lastname)s,
                                         password = %(password)s,
                                         email = %(email)s,
                                         permissions = %(permissions)s,
                                         type_id = %(type_id)s, 
                                         cellar_permissions = %(cellar_permissions)s 
                        where id = %(id)s'''
                p = {
                    "name":self.name,
                    "email":self.email,
                    "permissions":permisos,
                    "password":self.password,
                    "id":self.id,
                    "type_id": self.type_id,
                    "cellar_permissions":bodegas,
                    "lastname":self.lastname
                }
                cur.execute(q,p)
                self.connection.commit()
                return self.ShowSuccessMessage(str(self.id))
            else:

                q = '''\
                    insert into "User" (name,
                                        password,
                                        email,
                                        permissions,
                                        type_id,
                                        cellar_permissions,
                                        lastname) 
                    values (%(name)s,
                            %(password)s,
                            %(email)s,
                            %(permissions)s,
                            %(type_id)s,
                            %(cellar_permissions)s,
                            %(lastname)s) 
                    returning id'''
                p = {
                    "name":self.name,
                    "lastname":self.lastname,
                    "email":self.email,
                    "permissions":permisos,
                    "password":self.password,
                    "type_id": self.type_id,
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
        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            q = '''\
                select  u.*, 
                        STRING_AGG(distinct p.name, ',') as permissions_name, 
                        STRING_AGG(distinct c.name, ',') as cellars_name,
                        ut.name as type,
                        ut.id as type_id
                from "User" u 
                inner join "Permission" p on p.id = any(u.permissions) 
                inner join "Cellar" c on c.id = any(u.cellar_permissions) 
                inner join "User_Types" ut on ut.id = u.type_id
                where ut.id = any(%(user_type)s)
                group by u.id, ut.name, ut.id limit %(limit)s offset %(offset)s'''
            p = {
                "limit":items,
                "offset":offset,
                "user_type": [UserType.ADMINISTRADOR, UserType.GESTION, UserType.BODEGA]
            }
            cur.execute(q,p)

            lista = cur.fetchall()
            return lista
        except Exception,e:
            print str(e)
            return {}
