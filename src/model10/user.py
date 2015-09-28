#!/usr/bin/python
# -*- coding: UTF-8 -*-
from lp.model.basemodel import BaseModel as lp_model
from basemodel import BaseModel
import psycopg2
import psycopg2.extras
import random
#from ..handler.sendpassword import Email
import hashlib


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

        if self.id != "":

            cur = self.connection.cursor()
            q = '''delete from "User" where id = %(id)s'''.format(tabla=self.table)
            p = {
                "id":self.id
            }
            try:
                cur.execute(q,p)
                self.connection.commit()
                return self.ShowSuccessMessage("object: {} has been deleted".format(self.id))
            except Exception, e:
                return self.ShowError("object: not found, error:{}".format(str(e)))
            finally:
                cur.close()
                self.connection.close()
        else:
            return self.ShowError("identifier not found")

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
                    array_agg(distinct c.id) as cellars,
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
                self.name = usuario["name"]
                self.lastname = usuario["lastname"]
                self.identifier = usuario["id"]
                self.password = usuario["password"]
                self.permissions = usuario["permissions"]
                self.email = usuario["email"]
                self.id = usuario["id"]
                self.cellars = usuario["cellars"]
                self.cellars_name = usuario["cellars_name"]
                self.permissions_name = usuario["permissions_name"]
                self.type_id = usuario["type_id"]
                self.type = usuario["type"]
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
                    array_agg(distinct c.id) as cellars,
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
            self.name = usuario["name"]
            self.lastname = usuario["lastname"]
            self.identifier = usuario["id"]
            self.password = usuario["password"]
            self.permissions = usuario["permissions"]
            self.email = usuario["email"]
            self.id = usuario["id"]
            self.cellars = usuario["cellars"]
            self.cellars_name = usuario["cellars_name"]
            self.permissions_name = usuario["permissions_name"]
            self.type_id = usuario["type_id"]
            self.type = usuario["type"]
            return self.ShowSuccessMessage(usuario)
        except:
            return self.ShowError("user : " + idd + " not found")

    def Save(self):

        items_query_anterior = 0

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        q = '''select * from "User" where email = %(email)s and type_id = any(%(type_id)s) limit 1'''
        p = {
            "email":self.email,
            "type_id": [UserType.ADMINISTRADOR, UserType.GESTION, UserType.BODEGA]
        }

        try:
            cur.execute(q,p)
            usuario = cur.fetchone()
            items_query_anterior = cur.rowcount
        except Exception, e:
            return self.ShowError("error finding user {}".format(str(e)))
        finally:
            cur.close()
            self.connection.close()

        permisos = []

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

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # print permisos
        if items_query_anterior > 0:

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
                "cellar_permissions": [int(cellar_id) for cellar_id in self.cellars],
                "lastname":self.lastname
            }

            try:
                cur.execute(q,p)
                self.connection.commit()
                return self.ShowSuccessMessage(str(self.id))
            except Exception,e:
                return self.ShowError("failed to save user {}, error:{}".format(self.email,str(e)))
            finally:
                cur.close()
                self.connection.close()
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
                "cellar_permissions": [int(cellar_id) for cellar_id in self.cellars]
            }

            try:
                cur.execute(q,p)
                self.connection.commit()
                self.id = cur.fetchone()["id"]

                return self.ShowSuccessMessage(str(self.id))

            except Exception,e:
                return self.ShowError("failed to save user {}, error:{}".format(self.email,str(e)))
            finally:
                cur.close()
                self.connection.close()

    def GetList(self, page=1, items=30):

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

    def Exist(self, email='', _id=0):


        if email != "":

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            q = '''\
                select count(*) as cnt from "User" 
                where email = %(email)s 
                and type_id = any(%(type_id)s)
                and status = %(status)s'''

            p = { 
                "email" : email,
                "type_id": [self.getUserTypeID(UserType.CLIENTE), 
                            self.getUserTypeID(UserType.VISITA)],
                "status": self.ACEPTADO
            }

            try:
                # print cur.mogrify(q, p)
                cur.execute( q, p )
                data = cur.fetchone()
                if data["cnt"] > 0:
                    return self.ShowSuccessMessage(True)
                else:
                    return self.ShowSuccessMessage(False)
            except Exception, e:
                print "exists, {}".format(str(e))
                return self.ShowError(str(e))
            finally:
                cur.close()
                self.connection.close()

        if _id != 0:

            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            q = '''select count(*) as cnt from "User" where id = %(id)s and (type_id = %(user_type)s or type_id = %(user_type_visita)s)'''
            p = { 
                "id": _id,
                "user_type": self.getUserTypeID(UserType.CLIENTE),
                "user_type_visita": self.getUserTypeID(UserType.VISITA)
            }

            try:
                cur.execute(q,p)
                data = cur.fetchone()
                if data["cnt"] > 0:
                    return self.ShowSuccessMessage(True)
                else:
                    return self.ShowSuccessMessage(False)
            except Exception,e:
                return self.ShowError(str(e))
            finally:
                cur.close()
                self.connection.close()

    def ChangePassword(self, id, password):
        try:

            p = '''\
                update "User" 
                set password = %(password)s 
                where id = %(id)s and type_id = any(%(type_id)s)'''
            q = { 
                "id": id, 
                "password" : password,
                "type_id": [
                    self.getUserTypeID(UserType.CLIENTE), 
                    self.getUserTypeID(UserType.VISITA),
                    self.getUserTypeID(UserType.EMPRESA)
                ]
            }

            # c

            cur = self.connection.cursor( cursor_factory=psycopg2.extras.DictCursor )
            cur.execute( p,q )
            self.connection.commit()

        except Exception, e:
            print str( e )
            raise Exception( "no se ha podido cambiar la contraseña" )

    def getUserTypeID(self, user_type):

        query = '''SELECT id FROM "User_Types" WHERE name = %(name)s'''
        params = {"name" : user_type}
        return lp_model.execute_query(query, params)[0]["id"]

    def RandomPass(self):

        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        mypw = ""

        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]

    def PassRecovery( self, email ):
        try:
            exists = self.Exist( email )

            if "success" in exists:
                if exists["success"]:

                    password = ""
                    user_id = ""

                    p = ''' select name, password, id from "User" 
                    where email = %(email)s 
                    and (type_id = %(user_type)s or type_id = %(user_type_visita)s)'''
                    q = {
                        "email": email,
                        "user_type": self.getUserTypeID(UserType.CLIENTE),
                        "user_type_visita": self.getUserTypeID(UserType.VISITA)
                    }

                    cur = self.connection.cursor(  cursor_factory=psycopg2.extras.RealDictCursor )

                    cur.execute(p,q)
                    data = cur.fetchone()

                    password = data["password"]
                    user_id = "{}".format(data["id"])
                    name = data["name"]

                    new_password = self.RandomPass()

                    m = hashlib.md5()

                    m.update(new_password)

                    password = m.hexdigest()

                    self.ChangePassword(user_id,password)

                    Email( email, user_id, new_password, name )

                    return True

                else:
                    return False
            else:
                print exists["error"]
                raise Exception( "no se ha podido recuperar la contraseña, {}".format(exists["error"]) )
        except Exception, e:
            print "no se ha podido recuperar la contrasena : {}".format(str( e ))
            raise Exception( "no se ha podido recuperar la contraseña" )

        return mypw
