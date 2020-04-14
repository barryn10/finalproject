import pymysql
from baseObject import baseObject
class productList(baseObject):
    def __init__(self):
        self.setupObject('sharkbd_products')

    def verifyNew(self,n=0):
        self.errorList = []

        if len(self.data[n]['Name']) == 0:
            self.errorList.append("Name of product cannot be blank.")

        if len(self.data[n]['SKU']) == 0:
            self.errorList.append("Product SKU cannot be blank.")

        if len(self.data[n]['Price']) == 0:
            self.errorList.append("Price cannot be blank.")

        if len(self.errorList) > 0:
            return False
        else:
            return True
