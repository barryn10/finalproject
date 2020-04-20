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

        if len(self.data[n]['Type']) == 0:
            self.errorList.append("User must specify whether they are an admin or customer.")

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



        #Add unit tests
        #Add if statements for validation of other fields
