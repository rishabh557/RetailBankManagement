from application import app
from flask import render_template
from .models import Cashier, Executive, Accounts, db, Transaction, Customer, login_manager, login_required, login_user, SQLAlchemy
from flask import Flask, flash, render_template, redirect, url_for, request


@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/executivelogin')
def executivelogin():
    return render_template('executivelogin.html')

@app.route('/cashierlogin')
def cashierlogin():
    return render_template('cashierlogin.html')

@app.route('/executivehome')
def executivehome():
    return render_template('executivehome.html')

@app.route('/cashierhome')
def cashierhome():
    return render_template('cashierhome.html')

@app.route('/cashierauth', methods=['GET', 'POST'])
def cashierauth():
    username = request.form['username']
    user = Cashier.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return render_template('cashierhome.html')
    else:
        return "No records found"

@app.route('/executiveauth', methods=['POST'])
def executiveauth():
    username = request.form['username']
    user = Executive.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return render_template('executivehome.html')
    else:
        return "No records found"



@login_manager.user_loader
def load_executive(username):
    return Executive.query.get(username)


@login_manager.user_loader
def load_cashier(username):
    return Cashier.query.get(username)


@app.route('/createcustomer', methods =['GET', 'POST'])
def createcustomer():
    if request.method == 'POST':
        if not request.form['ssn'] or not request.form['cust_id'] or not request.form['name'] or not request.form['address'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            customer = Customer(request.form['ssn'], request.form['cust_id'], request.form['name'], request.form['address'], request.form['age'])
            db.session.add(customer)
            db.session.commit()
            flash('Record was successfully added')
            return render_template('executivehome.html')



@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        if not request.form['acc_number'] or not request.form['acc_type'] or not request.form['balance'] or not request.form['cust_id']:
            flash('Please enter all the fields', 'error')
        else:
            account = Accounts(request.form['acc_number'], request.form['acc_type'], request.form['balance'], request.form['cust_id'])
            db.session.add(account)
            db.session.commit()
            flash('Record was successfully added')
            return render_template('executivehome.html')

