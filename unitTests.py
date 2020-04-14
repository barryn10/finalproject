from user import userList
import time
ul = userList() #instance of a customer list class (object)

#Be familiar with set, add, insert,delete,update, .data

ul.set('userFirst','Bobby')
ul.set('userLast','Joe')
ul.set('userEmail','bjoe@aol.com')
ul.set('userPassword','12345')
ul.set('userType','Customer')
ul.add()
ul.insert()

'''
print(cl.errorList)
'''
#DB is blank right now,
'''
cl.insert()
print(cl.data)
time.sleep(10)
cl.delete()
print(cl.data)
'''
'''
print(cl.data)
print(cl.data[0])
#cl.update(0,'email','b@b.com')
#cl.update(0,'e_mail','b@b.com')
print(cl.data)

cl.insert()
'''
