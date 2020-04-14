from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response
from user import userList
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

    return render_template('welcomepage.html', title='Welcome!')


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

@app.route('/logincustomer', methods = ['GET','POST'])
def logincustomer():
    if request.form.get('email') is not None and request.form.get('password') is not None:
        u = userList()
        if c.tryLogin(request.form.get('email'),request.form.get('password')):
            #print('login ok')
            session['user'] = c.data[0]
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
        return render_template('logincustomer.html', title='Login', msg=m)

@app.route('/loginadmin', methods = ['GET','POST'])
def loginadmin():
    if request.form.get('email') is not None and request.form.get('password') is not None:
        u = userList()
        if c.tryLogin(request.form.get('email'),request.form.get('password')):
            #print('login ok')
            session['user'] = c.data[0]
            session['active'] = time.time()

            return redirect('main')
        else:
            #print('login failed')
            return render_template('loginadmin.html', title='Login', msg='Incorrect username or password.')
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
    return render_template('customers.html', title='Customer List',user=u.data)

@app.route('/customer')
def customer():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    if request.args.get(c.pk) is None:
        return render_template('error.html', msg='No customer id given.')


    c.getById(request.args.get(c.pk))
    if len(u.data) <= 0:
        return render_template('error.html', msg='Customer not found.')

    print(u.data)
    #return ''
    return render_template('customer.html', title='Customer ',user=u.data[0])
@app.route('/newcustomer',methods = ['GET', 'POST'])
def newcustomer():
    if checkSession() == False:
        return redirect ('login')
    if request.form.get('userFirst') is None:
        u = userList()
        u.set('userFirst','')
        u.set('userLast','')
        u.set('userEmail','')
        u.set('userPassword','')
        u.set('userType','')
        u.add()
        return render_template('newcustomer.html', title='New Customer', user=u.data[0])
    else:
        u = userList()
        u.set('userFirst',request.form.get('userFirst'))
        u.set('userLast',request.form.get('userLast'))
        u.set('userEmail',request.form.get('userEmail'))
        u.set('userPassword',request.form.get('userPassword'))
        u.set('userType',request.form.get('userType'))
        u.add()
        if u.verifyNew():
            u.insert()
            print(u.data)
            return render_template('savedcustomer.html', title='Customer Saved',user=u.data[0])
        else:
            return render_template('newcustomer.html', title='Customer Not Saved',user=u.data[0],msg=u.errorList)

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
            print(u.data)
            return render_template('savedcustomer.html', title='User Saved',user=u.data[0])
        else:
            return render_template('brandnewuser.html', title='User Not Saved',user=u.data[0],msg=u.errorList)


@app.route('/savecustomer',methods = ['GET', 'POST'])
def savecustomer():
    if checkSession() == False:
        return redirect('login')
    u = userList()
    u.set('userID',request.form.get('userID'))
    u.set('userFirst',request.form.get('userFirst'))
    u.set('userLast',request.form.get('userLast'))
    u.set('userEmail',request.form.get('userEmail'))
    u.set('UserPassword',request.form.get('userPassword'))
    u.set('userType',request.form.get('userType'))
    u.add()
    u.update()
    print(u.data)
        #return ''
    return render_template('savedcustomer.html', title='Customer Saved',user=u.data[0])

@app.route('/main')
def main():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    userinfo = 'Hello, ' + session['user']['First']
    return render_template('main.html', title='Main menu',msg = userinfo)

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

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)
