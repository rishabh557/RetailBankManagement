from application import app
from flask import render_template
from .models import Cashier, Executive, Accounts, db, Transaction, Customer, login_manager, login_required, login_user, SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request, flash


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


@app.route('/createcustomer', methods = ['GET', 'POST'])
def createcustomer():
    if request.method == 'POST':
        if not request.form['ssn'] or not request.form['cust_id'] or not request.form['name'] or not request.form['address'] or not request.form['age']:
            flash('Please enter all the fields' , 'error')
        else:
            customer = Customer(request.form['ssn'], request.form['cust_id'], request.form['name'], request.form['address'], request.form['age'])
            db.session.add(customer)
            db.session.commit()
            flash('Record was successfully added')
            return render_template('executivehome.html')



@app.route('/createaccount', methods = ['GET', 'POST'])
def createaccount():
    if request.method == 'POST':
        if not request.form['acc_number'] or not request.form['acc_type'] or not request.form['balance'] or not request.form['cust_id']:
            flash('Please enter all the fields' , 'error')
        else:
            account = Accounts(request.form['acc_number'], request.form['acc_type'], request.form['balance'], request.form['cust_id'])
            db.session.add(account)
            db.session.commit()
            flash('Record was successfully added')
            return render_template('executivehome.html')


@app.route('/getaccountdetails', methods=['GET','POST'])
def getaccountdetails():
    return render_template('getaccdetails.html')


@app.route('/accdetails', methods=['GET', 'POST'])
def accdetails():
    cust_ssn_ID = int(request.form['custID'])
    accID = request.form['accID']
    if accID:
        is_valid_acc = Accounts.query.filter_by(acc_number=accID).first()
        if is_valid_acc is not None:
            details = Accounts.query.get(accID)
            return render_template('displayaccdetails.html', details=details)
    elif cust_ssn_ID:
        print("TESTED")
        is_valid_ssn = Customer.query.filter_by(ssn=cust_ssn_ID).first()
        is_valid_cust = Customer.query.filter_by(cust_id=cust_ssn_ID).first()
        if is_valid_cust is not None:
            details = Accounts.query.filter_by(cust_id=cust_ssn_ID)
            return render_template('displayaccdetails.html', details=details)
        elif is_valid_ssn is not None:
            cust_details = Customer.query.get(cust_ssn_ID)
            details = Accounts.query.filter_by(cust_id=cust_details.cust_id)
            return render_template('displayaccdetails.html', details=details)
    else:
        flash("Please enter a valid Customer ID/Account Number")
    return redirect(url_for('getaccountdetails'))
