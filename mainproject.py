from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response
from user import userList
from product import productList
from orders import orderList
from cart import cartList
import pymysql
import json
import time

from flask_session import Session #serverside sessions

app = Flask(__name__,static_url_path='')

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'

@app.route('/get')
def get():
    return str(session['time'])

@app.route('/thesneakerstore')
def thesneakerstore():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    allProducts = productList()
    allProducts.getAll()

    u = userList()
    p = productList()
    c = cartList()
    c.set('userID',session['user']['userID'])
    p.getAll()


    print(p.data)


    return render_template('purchase.html', title='Check out our shoe selection!',products=p.data,user=u.data,pl=allProducts.data,cart=c.data)

@app.route('/storecart', methods = ['GET','POST'])
def storecart():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    allProducts = productList()
    allProducts.getAll()
    if request.form.get('cart') is None:
        p = productList()
        c = cartList()
    #if request.args.get(p.pk) is None:
        #return render_template('error.html', msg='No product id given.')
        c.set('cartID','')
        c.set('productID','')
        c.set('userID','')
        c.add()
        c.getAll()
        return render_template('storecart.html', title='Here is your cart contents!',product=p.data,carts=c.data,pl=allProducts.data)
    else:
        #p.getById(request.args.get(p.pk))
        #if len(p.data) <= 0:
            #return render_template('error.html', msg='Product not found.')
        c = cartList()
        c.set('cartID',request.form.get('cartID'))
        c.set('productID',request.form.get('productID'))
        c.set('userID',request.form.get(session['user']['userID']))
        #p.set('productShoeHeight',request.form.get('productShoeHeight'))
        c.add()
        if c.verifyNew():
            c.insert()
            c.getAll()
            print(c.data)
            return render_template('storecart.html', title='Here is your cart contents!',product=p.data,carts=c.data)
        else:
            return render_template('purchase.html', title='Here is your cart contents!',product=p.data,carts=c.data)

@app.route('/cart')
def cart():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    #sneakerwelcome = 'Hello, ' + session['user']['First'] + ' ' + 'I hope you are ready to shop today. Welcome to our store!'
    c = cartList()
    if request.args.get(c.pk) is None:
        return render_template('error.html', msg='No id given.')

    c.getById(request.args.get(c.pk))
    if len(c.data) <= 0:
        return render_template('error.html', msg='Product not found.')

    c.update()
    print(c.data)

    #print(c.data)
    return render_template('cartedit.html', title='Orders',msg ='',cart=c.data[0])

@app.route('/login', methods = ['GET','POST'])
def login():
    print ('dcdcckdmkcdmcdkcmdmckdmckdkmc')
    if request.form.get('Email') is not None and request.form.get('Password') is not None:
        u = userList()
        if u.tryLogin(request.form.get('Email'),request.form.get('Password')):
            #print('login ok')
            session['user'] = u.data[0]
            session['active'] = time.time()

            return redirect('main')
        else:
            #print('login failed')
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)

@app.route('/logout', methods = ['GET','POST'])
def logout():
    del session['user']
    del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')


@app.route('/basichttp')
def basichttp():
    if request.args.get('myvar') is not None:
        a = request.args.get('myvar')
        return 'your var:' + request.args.get('myvar')
    else:
        return 'myvar not set'

@app.route('/')
def home():
    return render_template('test.html', title='Test2', msg='Welcome!')

@app.route('/index')
def index():
    user = {'username': 'Tyler'}

    items = [
        {'name':'Apple','price':2.34},
        {'name':'Orange','price':4.88},
        {'name':'Grape','price':2.44}
    ]
    return render_template('index.html', title='Home', user=user, items=items)

@app.route('/customers')
def customers():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    u = userList()
    u.getAll()


    print(u.data)
    #return ''
    return render_template('customers.html', title='Customer List',users=u.data)

@app.route('/user')
def user():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    if request.args.get(u.pk) is None:
        return render_template('error.html', msg='No customer id given.')


    u.getById(request.args.get(u.pk))
    if len(u.data) <= 0:
        return render_template('error.html', msg='Customer not found.')


    u.update()
    print(u.data)
    #return ''
    return render_template('user.html', title='Customer ',user=u.data[0])

@app.route('/product')
def product():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    if request.args.get(p.pk) is None:
        return render_template('error.html', msg='No product id given.')

    p.getById(request.args.get(p.pk))
    if len(p.data) <= 0:
        return render_template('error.html', msg='Product not found.')

    p.update()
    print(p.data)

    return render_template('productedit.html', title='Customer ',product=p.data[0])


    #p.update()
    #p.verifyNew()
    #return ''

@app.route('/newproduct',methods = ['GET','POST'])
def newproduct():
    print ('dcdcckdmkcdmcdkcmdmckdmckdkmc')
    if checkSession() == False:
        return redirect('login')
    p = productList()
    if request.form.get('productName') is None:
        p = productList()
        p.set('productName','')
        p.set('productSize','')
        p.set('productShoeHeight','')
        p.add()

        return render_template('newproduct.html', title='New Product.', product=p.data[0])
    else:
        p = productList()
        p.set('productName',request.form.get('productName'))
        p.set('productSize',request.form.get('productSize'))
        p.set('productShoeHeight',request.form.get('productShoeHeight'))
        p.add()
        if p.verifyNew():
            p.insert()
            print(p.data)
            return render_template('savedproduct.html', title='Product Saved.',product=p.data[0])
        else:
            return render_template('newproduct.html', title='Product Not Saved.',product=p.data[0],msg=p.errorList)

    #p.update()
    #p.verifyNew()
    #return ''

@app.route('/newcustomer',methods = ['GET', 'POST'])
def newcustomer():
    if checkSession() == False:
        return redirect ('login')
    if request.form.get('First') is None:
        u = userList()
        u.set('First','')
        u.set('Last','')
        u.set('Email','')
        u.set('Password','')
        u.set('Type','')
        u.add()
        return render_template('newcustomer.html', title='New Customer',user=u.data[0])
    else:
        u = userList()
        u.set('First',request.form.get('First'))
        u.set('Last',request.form.get('Last'))
        u.set('Email',request.form.get('Email'))
        u.set('Password',request.form.get('Password'))
        u.set('Type',request.form.get('Type'))
        u.add()
        if u.verifyNew():
            u.insert()
            print(u.data)
            return render_template('savedcustomer.html', title='Customer Saved',user=u.data[0])
        else:
            return render_template('newcustomer.html', title='Customer Not Saved',user=u.data[0],msg=u.errorList)

@app.route('/neworder',methods = ['GET', 'POST'])
def neworder():
        if checkSession() == False:
            return redirect ('login')
        allProducts = productList()
        allProducts.getAll()
        if request.form.get('order') is None:
            p = productList()
            o = orderList()
            o.set('userID','')
            o.set('productID','')
            o.set('productName','')
            o.set('productSize','')
            o.set('Customer','')
            o.set('Address','')
            o.set('cardType','')
            o.add()
            return render_template('createOrder.html', title='New Order',order=o.data[0],pl=allProducts.data,product=p.data)
        else:
            o = orderList()
            o.set('userID',session['user']['userID'])
            o.set('productID',request.form.get('productID'))
            o.set('productName',request.form.get('productName'))
            o.set('productSize',request.form.get('productSize'))
            o.set('Customer',request.form.get('Customer'))
            o.set('Address',request.form.get('Address'))
            o.set('cardType',request.form.get('cardType'))
            o.add()
            if o.verifyNew():
                o.insert()
                print(o.data)
                return render_template('savedorder.html', title='Order Saved',order=o.data[0])
            else:
                return render_template('createOrder.html', title='Order Not Saved',order=o.data[0],msg=u.errorList)
@app.route('/brandnewuser',methods = ['GET', 'POST'])
def brandnewuser():
    if request.form.get('First') is None:
        u = userList()
        u.set('First','')
        u.set('Last','')
        u.set('Email','')
        u.set('Password','')
        u.set('Type','')
        u.add()
        return render_template('brandnewuser.html', title='New User', user=u.data[0])
    else:
        u = userList()
        u.set('First',request.form.get('First'))
        u.set('Last',request.form.get('Last'))
        u.set('Email',request.form.get('Email'))
        u.set('Password',request.form.get('Password'))
        u.set('Type',request.form.get('Type'))
        u.add()
        if u.verifyNew():
            u.insert()
            #print(u.data)
            return render_template('savednewcustomer.html', title='User Saved',user=u.data[0])
        else:
            return render_template('brandnewuser.html', title='User Not Saved',user=u.data[0],msg=u.errorList)


@app.route('/savecustomer',methods = ['GET', 'POST'])
def savecustomer():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    u.set('userID',request.form.get('userID'))
    u.set('First',request.form.get('First'))
    u.set('Last',request.form.get('Last'))
    u.set('Email',request.form.get('Email'))
    u.set('Password',request.form.get('Password'))
    u.set('Type',request.form.get('Type'))
    u.add()
    u.update()
    #u.insert()
    print(u.data)
        #return ''
    return render_template('savedcustomer.html', title='Customer Saved',user=u.data[0])

@app.route('/saveproduct',methods = ['GET', 'POST'])
def saveproduct():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    p.set('productID',request.form.get('productID'))
    p.set('productName',request.form.get('productName'))
    p.set('productSize',request.form.get('productSize'))
    p.set('productShoeHeight',request.form.get('productShoeHeight'))
    p.add()
    p.update()
    #p.insert()
    print(p.data)
        #return ''
    return render_template('savedproduct.html', title='Product Saved',product=p.data[0])


@app.route('/savecart',methods = ['GET', 'POST'])
def savecart():
    if checkSession() == False:
        return redirect('login')
    p = productList()
    c = cartList()
    c.set('cartID',request.form.get('cartID'))
    c.set('productID',request.form.get('productID'))
    c.set('userID',request.form.get(session['user']['userID']))
    c.add()
    c.insert()
    print('aaaaaaaaaaaaaa')
    print(c.data)
    c.getAll()
        #return ''
    return render_template('savedcart.html', title='Shoe added to your cart.',products=p.data,cart=c.data)


@app.route('/main')
def main():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('loginadmin')
    userinfo = 'Hello, ' + session['user']['First'] + ' ' +session['user']['Last'] + ' (' +session['user']['Type'] +')'
    if session['user']['Type'] == 'Admin':
        return render_template('main.html', title='Main menu',msg = userinfo)
    if session['user']['Type'] == 'Customer':
        return render_template('maincustomer.html', title='Main menu',msg = userinfo)

@app.route('/maincustomer')
def maincustomer():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    userinfo = 'Hello, ' + session['user']['First'] + ' ' +session['user']['Last']
    return render_template('maincustomer.html', title='Main menu',msg = userinfo)

@app.route('/products')
def products():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    #sneakerwelcome = 'Hello, ' + session['user']['First'] + ' ' + 'I hope you are ready to shop today. Welcome to our store!'
    p = productList()
    p.getAll()
    print(p.data)
    return render_template('products.html', title='Sneakers',msg ='',products=p.data)

@app.route('/viewproducts')
def viewproducts():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    #sneakerwelcome = 'Hello, ' + session['user']['First'] + ' ' + 'I hope you are ready to shop today. Welcome to our store!'
    p = productList()
    p.getAll()
    print(p.data)
    return render_template('viewproducts.html', title='Sneakers',msg ='',products=p.data)

@app.route('/orders')
def orders():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    #sneakerwelcome = 'Hello, ' + session['user']['First'] + ' ' + 'I hope you are ready to shop today. Welcome to our store!'
    o = orderList()
    o.getAll()
    print(o.data)
    return render_template('orders.html', title='Orders',msg ='',orders=o.data)

@app.route('/myorders')
def myorders():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    #sneakerwelcome = 'Hello, ' + session['user']['First'] + ' ' + 'I hope you are ready to shop today. Welcome to our store!'
    o = orderList()
    o.getAll()
    print(o.data)
    return render_template('myorders.html', title='Orders',msg ='',orders=o.data)

@app.route('/createOrder',methods = ['GET', 'POST'])
def createOrder():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    allProducts = productList()
    allProducts.getAll()
    u = userList()
    o = orderList()
    p = productList()
    if request.form.get('productID') is None:
        o = orderList()
        o.set('productID','')
        #o.set('productName','')
        #o.set('productSize','')
        o.set('Customer','')
        o.set('Address','')
        o.set('cardType','')
        o.add()
        return render_template('createOrder.html', title='New Order',order=o.data[0],product=p.data[0])
    else:
        o = orderList()
        o.set('productID',request.form.get('productID'))
        #o.set('productName',request.form.get('productName'))
        #o.set('productSize',request.form.get('productSize'))
        o.set('Customer',request.form.get('Customer'))
        o.set('Address',request.form.get('Address'))
        o.set('cardType',request.form.get('cardType'))

        o.add()
        #if o.verifyNew():
            #o.insert()
            #print(o.data)
            #return render_template('savedorder.html', title='Order Saved',order=o.data[0])
        #else:
            #return render_template('createOrder.html', title='Order Not Saved',order=o.data[0],msg=u.errorList)

    '''if request.args.get(p.pk) is None:
        return render_template('error.html', msg='No customer id given.')


    p.getById(request.args.get(p.pk))
    if len(p.data) <= 0:
        return render_template('error.html', msg='Customer not found.')


    p.update()
    print(p.data)
'''
    #sneakerwelcome = 'Hello, ' + session['user']['First'] + ' ' + 'I hope you are ready to shop today. Welcome to our store!'

    return render_template('createOrder.html', title='Creating an order...',msg ='',order=o.data,product=p.data,user=u.data)

@app.route('/createOrderByProduct',methods = ['GET', 'POST'])
def createOrderByProduct():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    allProducts = productList()
    allProducts.getAll()
    u = userList()
    o = orderList()
    p = productList()
    if request.form.get('productID') is None:
        o = orderList()
        #o.set('productID','')
        o.set('productName','')
        o.set('productSize','')
        o.set('Customer','')
        o.set('Address','')
        o.set('cardType','')
        o.add()
        return render_template('createOrderByProduct.html', title='New Order',order=o.data[0],product=p.data[0])
    else:
        o = orderList()
        #o.set('productID',request.form.get('productID'))
        o.set('productName',request.form.get('productName'))
        o.set('productSize',request.form.get('productSize'))
        o.set('Customer',request.form.get('Customer'))
        o.set('Address',request.form.get('Address'))
        o.set('cardType',request.form.get('cardType'))

        o.add()
        #if o.verifyNew():
            #o.insert()
            #print(o.data)
            #return render_template('savedorder.html', title='Order Saved',order=o.data[0])
        #else:
            #return render_template('createOrder.html', title='Order Not Saved',order=o.data[0],msg=u.errorList)

    '''if request.args.get(p.pk) is None:
        return render_template('error.html', msg='No customer id given.')


    p.getById(request.args.get(p.pk))
    if len(p.data) <= 0:
        return render_template('error.html', msg='Customer not found.')


    p.update()
    print(p.data)
'''
    #sneakerwelcome = 'Hello, ' + session['user']['First'] + ' ' + 'I hope you are ready to shop today. Welcome to our store!'

    return render_template('createOrderByProduct.html', title='Creating an order...',msg ='',order=o.data,product=p.data,user=u.data)


@app.route('/saveorder',methods = ['GET', 'POST'])
def saveorder():
    if checkSession() == False:
        return redirect('login')
    o = orderList()
    o.set('orderID',request.form.get('orderID'))
    o.set('productID',request.form.get('productID'))
    #o.set('productName',request.form.get('productName'))
    #o.set('productSize',request.form.get('productSize'))
    o.set('Customer',request.form.get('Customer'))
    o.set('Address',request.form.get('Address'))
    o.set('cardType',request.form.get('cardType'))
    o.set('orderStatus',request.form.get('orderStatus'))
    o.add()
    o.update()
    #o.insert()
    #p.insert()
    print(o.data)
        #return ''
    return render_template('savedorder.html', title='Order Saved',order=o.data[0])

@app.route('/order')
def order():
    if checkSession() == False:
        return redirect('login')
    o = orderList()
    if request.args.get(o.pk) is None:
        return render_template('error.html', msg='No product id given.')

    o.getById(request.args.get(o.pk))
    if len(o.data) <= 0:
        return render_template('error.html', msg='Product not found.')

    #o.update()
    print(o.data)

    return render_template('orderedit.html', title='Order ',order=o.data[0])


def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False

def checkShoppingCart():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your item is no longer in your cart.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False

@app.route('/deleteuser',methods = ['GET', 'POST'])
def deleteuser():
    if checkSession() == False:
        return redirect('login')
    print("userID:",request.form.get('userID'))
    #return ''
    u = userList()
    u.deleteByID(request.form.get('userID'))
    return render_template('confirmaction.html', title='Customer Deleted',  msg='Customer deleted.')

    '''
    <form action="/deletecustomer" method="POST">
			<input type="submit" value="Delete this customer" />
			<input type="hidden" name="id" value="{{ customer.id }}" />
		</form>
    '''

@app.route('/deleteproduct',methods = ['GET', 'POST'])
def deleteproduct():
    if checkSession() == False:
        return redirect('login')
    print("productID:",request.form.get('productID'))
    #return ''
    p = productList()
    p.deleteByID(request.form.get('productID'))
    return render_template('confirmaction.html', title='Product Deleted',  msg='Product deleted.')

    '''
    <form action="/deletecustomer" method="POST">
			<input type="submit" value="Delete this customer" />
			<input type="hidden" name="id" value="{{ customer.id }}" />
		</form>
    '''

@app.route('/deleteorder',methods = ['GET', 'POST'])
def deleteorder():
    if checkSession() == False:
        return redirect('login')
    print("orderID:",request.form.get('orderID'))
    #return ''
    o = orderList()
    o.deleteByID(request.form.get('orderID'))
    return render_template('confirmaction.html', title='Order Deleted',  msg='Order deleted.')

    '''
    <form action="/deletecustomer" method="POST">
			<input type="submit" value="Delete this customer" />
			<input type="hidden" name="id" value="{{ customer.id }}" />
		</form>
    '''

@app.route('/deletecart',methods = ['GET', 'POST'])
def deletecart():
    if checkSession() == False:
        return redirect('login')
    print("cartID:",request.form.get('cartID'))
    #return ''
    c = cartList()
    c.deleteByID(request.form.get('cartID'))
    return render_template('confirmaction.html', title='Cart entry Deleted',  msg='Cart entry deleted.')

    '''
    <form action="/deletecustomer" method="POST">
			<input type="submit" value="Delete this customer" />
			<input type="hidden" name="id" value="{{ customer.id }}" />
		</form>
    '''



@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)
