import pymysql
from baseObject import baseObject
class cartList(baseObject):
    def __init__(self):
        self.setupObject('sharkbd_cart')

    def verifyNew(self,n=0):
        self.errorList = []

        if len(self.data[n]['Quantity']) < 1 or > 5:
            self.errorList.append("Quantity must be at least 1 and no greater than 5.")

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
