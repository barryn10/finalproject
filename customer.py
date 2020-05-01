import pymysql
from baseObject import baseObject
class productList(baseObject):
    def __init__(self):
        self.setupObject('sharkbd_products')

    def verifyNew(self,n=0):
        self.errorList = []

        if len(self.data[n]['productName']) < 10:
            self.errorList.append("Name of product must be at least 10 characters long.")

        if len(self.data[n]['productSize']) == 0:
            self.errorList.append("Product Size cannot be blank.")

        if (self.data[n]['productShoeHeight']) == 0:
            self.errorList.append("Shoe Height must be entered as low, mid, or high.")

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
