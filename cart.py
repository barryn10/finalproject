import pymysql
from baseObject import baseObject
class cartList(baseObject):
    def __init__(self):
        self.setupObject('sharkbd_cart')

    def verifyNew(self,n=0):
        self.errorList = []

        if len(self.errorList) > 0:
            return False
        else:
            return True

    def getAll(self,order = None):
        sql = 'SELECT * FROM `' + self.tn + '` '
        if order != None:
            sql += 'ORDER BY `'+order+'`'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tokens)
        cur.execute(sql)
        self.data = []
        for row in cur:
            self.data.append(row)

    def insert(self,n=0):
        cols = ''
        vals = ''
        tokens = []
        for fieldname in self.fnl:
            if fieldname in self.data[n].keys():
                tokens.append(self.data[n][fieldname])
                vals += '%s,'
                cols += '`'+fieldname+'`,'
        vals = vals[:-1]
        cols = cols[:-1]
        sql = 'INSERT INTO `' + self.tn +'` (' +cols + ') VALUES (' + vals+');'
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tokens)
        cur.execute(sql,tokens)
        self.data[n][self.pk] = cur.lastrowid

    def delete(self,n=0):
        item = self.data.pop(n)
        self.deleteByID(item[self.pk])

    def add(self): #Add everything that has been set but won't be added to the DB
        self.data.append(self.tempdata)
    def set(self,fn,val):
        if fn in self.fnl:
            self.tempdata[fn] = val
        else:
            print('Invalid field: ' + str(fn))

    def update(self,n=0):
        tokens = []
        setstring = ''
        for fieldname in self.data[n].keys():
            if fieldname != self.pk:
                setstring += ' `'+fieldname+'` = %s,'
                tokens.append(self.data[n][fieldname])

        setstring = setstring[:-1]
        sql = 'UPDATE `' + self.tn + '` SET ' + setstring + ' WHERE `' + self.pk + '` = %s'
        tokens.append(self.data[n][self.pk])
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)

        #print(sql)
        #print(tokens)
        cur.execute(sql,tokens)
        #self.data[n][self.pk] = cur.lastrowid
    def deleteByID(self,id):
        sql = 'DELETE FROM`' + self.tn + '` WHERE `'+self.pk+'` = %s;'
        tokens = (id)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tokens)
