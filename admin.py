import pymysql
from baseObject import baseObject
class userList(baseObject):
    def __init__(self):
        self.setupObject('sharkbd_user')

    def verifyNew(self,n=0):
        self.errorList = []

        if len(self.data[n]['First']) == 0:
            self.errorList.append("First name cannot be blank.")

        if len(self.data[n]['Last']) == 0:
            self.errorList.append("Last name cannot be blank.")

        if len(self.data[n]['Email']) == 0:
            self.errorList.append("Password cannot be blank.")

        if len(self.data[n]['Password']) == 0:
            self.errorList.append("Email cannot be blank.")

        if len(self.errorList) > 0:
            return False
        else:
            return True
    def tryLogin(self,email,pw):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `email` = %s AND `password` = %s;'
        tokens = (email,pw)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tokens)
        cur.execute(sql,tokens)
        self.data = []
        n=0
        for row in cur:
            self.data.append(row)
            n+=1
        if n > 0:
            return True
        else:
            return False
    def tryAdmin(self,email,pw):
        sql = 'SELECT * FROM `' + self.tn + '` WHERE `email` = barryn@aol.com AND `password` = 12345;'
        #tokens = (email,pw)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print(tokens)
        cur.execute(sql,tokens)
        self.data = []
        n=0
        for row in cur:
            self.data.append(row)
            n+=1
        if n > 0:
            return True
        else:
            return False

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

    def deleteByID(self,id):
        sql = 'DELETE FROM`' + self.tn + '` WHERE `'+self.pk+'` = %s;'
        tokens = (id)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(sql,tokens)

    def getAdmins(self,id):
        '''
        SELECT * FROM `conlontj_products`
        LEFT JOIN `conlontj_products` ON `conlontj_products`.`productID` = `conlontj_orders`.`orderID`
        WHERE  `conlontj_attends`.`customer_id` = 3

        '''
        sql = '''SELECT * FROM `sharkbd_orders`
        LEFT JOIN `sharkbd_products` ON `sharkbd_products`.`productID` = `sharkbd_orders`.`productID`
        WHERE  `sharkbd_orders`.`productID` = %s'''
        tokens = (id)
        self.connect()
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        #print(sql)
        #print('tokens:',str(tokens))
        self.log(sql,tokens)
        cur.execute(sql,tokens)
        self.data = []
        for row in cur:
            self.data.append(row)




        #Add unit tests
        #Add if statements for validation of other fields
