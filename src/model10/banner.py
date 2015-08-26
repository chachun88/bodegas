#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemodel import BaseModel

import psycopg2
import psycopg2.extras


class Banner(BaseModel):

    def __init__(self):
        BaseModel.__init__(self)
        self._name = ''
        self._image = ''
        self._thumbnail = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def thumbnail(self):
        return self._thumbnail

    @thumbnail.setter
    def thumbnail(self, value):
        self._thumbnail = value

    def save(self):

        cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if self.id == '':
            query = '''\
                    insert into "Banner" (name, image, thumbnail)
                    values (%(name)s, %(image)s, %(thumbnail)s)
                    returning id
                    '''
            parametros = {
                "name": self.name,
                "image": self.image,
                "thumbnail": self.thumbnail
            }
        else:
            query = '''\
                    update "Banner"
                    set name = %(name)s, 
                        image = %(image)s, 
                        thumbnail = %(thumbnail)s
                    where id = %(id)s
                    returning id
                    '''
            parametros = {
                "name": self.name,
                "image": self.image,
                "thumbnail": self.thumbnail,
                "id": self.id
            }

        try:
            cur.execute(query, parametros)
            self.connection.commit()
            self.id = cur.fetchone()["id"]
            return self.id
        except Exception, e:
            # print str(e)
            return ''
        finally:
            cur.close()
            self.connection.close()

    def initByName(self, name=''):

        if name == '':
            return None
        else:
            cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = '''\
                    select id, name, image, thumbnail
                    from "Banner"
                    where name = %(name)s
                    limit 1'''
            parameters = {
                "name": name
            }

            try:
                cur.execute(query, parameters)
                self.connection.commit()
                banner = cur.fetchone()
                self.id = banner['id']
                self.name = banner['name']
                self.image = banner['image']
                self.thumbnail = banner['thumbnail']
                return banner
            except Exception, e:
                # print str(e)
                return None
            finally:
                cur.close()
                self.connection.close()
