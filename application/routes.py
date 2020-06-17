from application import app
from flask import render_template , session
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
        session['logged_in'] = True
        return render_template('getaccdetails.html')
    else:
        return "No records found"

@app.route('/executiveauth', methods=['POST'])
def executiveauth():
    username = request.form['username']
    user = Executive.query.filter_by(username=username).first()
    if user:
        login_user(user)
        session['logged_in'] = True
        return render_template('executivehome.html')
    else:
        return "No records found"

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.html')

@login_manager.user_loader
def load_executive(username):
    return Executive.query.get(username)


@login_manager.user_loader
def load_cashier(username):
    return Cashier.query.get(username)


@app.route('/createcustomer', methods=['GET','POST'])
def createcustomer():
    return render_template('createcustomer.html')

@app.route('/newcust', methods =['GET', 'POST'])
def newcust():
    if request.method == 'POST':
        if not request.form['ssn'] or not request.form['cust_id'] or not request.form['name'] or not request.form['address'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            customer = Customer(request.form['ssn'], request.form['cust_id'], request.form['name'], request.form['address'], request.form['age'])
            db.session.add(customer)
            db.session.commit()
            flash('Customer creation initiated successfully')
            return render_template('executivehome.html')

@app.route('/updatecust1', methods = ['GET', 'POST'])
def updatecust1():
    if request.method == 'POST':
        cust_id = request.form['custID']
        ssn_id = request.form['ssnID']
        if cust_id:
            cust_id=int(cust_id)
            is_valid_cust = Customer.query.filter_by(cust_id=cust_id).first()
            if is_valid_cust is not None:
                details = Customer.query.get(cust_id)
                return render_template('displaycustdetails.html', data = details)
        elif ssn_id:
            ssn_id=int(ssn_id)
            is_valid_ssn = Customer.query.filter_by(ssn=ssn_id).first()
            if is_valid_ssn is not None:
                details = Customer.query.get(ssn_id)
                return render_template('displaycustdetails.html', data = details)      
        else:
            flash("Please enter a valid Customer ID/SSN Number")

    return render_template('updatecustomer.html')


@app.route('/updatecust2', methods = ['GET', 'POST'])
def updatecust2():
    if request.method == 'POST':
        cust_id = int(request.form['custID'])
        is_valid_cust = Customer.query.filter_by(cust_id=cust_id).first()
        if is_valid_cust is not None:
            details = Customer.query.get(cust_id)
            details.name = request.form['name']
            details.address = request.form['address'] 
            details.age = request.form['age']
            db.session.commit()
            flash("Customer update initiated successfully")
    
    return render_template('updatecustomer.html')


@app.route('/deletecustomer', methods=['GET','POST'])
def deletecustomer():
    return render_template('deletecustomer.html')

@app.route('/deletecust', methods =['GET', 'POST'])
def deletecust():
    if request.method == 'POST':
        cust_id = int(request.form['cust_id'])
        is_valid_cust = Customer.query.filter_by(cust_id=cust_id).first()
        if is_valid_cust is not None:
            Customer.query.filter_by(cust_id=cust_id).delete()
            db.session.commit()
            flash('Customer deletion initiated successfully')
        else:
            flash('No record found')
            
    return render_template('deletecustomer.html')


@app.route('/createaccount', methods=['GET','POST'])
def createaccount():
        return render_template('createaccount.html')

@app.route('/newacc', methods=['GET', 'POST'])
def newacc():
    if request.method == 'POST':
        if not request.form['acc_number'] or not request.form['acc_type'] or not request.form['balance'] or not request.form['cust_id']:
            flash('Please enter all the fields', 'error')
        else:
            account = Accounts(request.form['acc_number'], request.form['acc_type'], request.form['balance'], request.form['cust_id'])
            db.session.add(account)
            db.session.commit()
            flash('Account creation initiated successfully')
            return render_template('executivehome.html')


@app.route('/deleteaccount', methods=['GET','POST'])
def deleteaccount():
    return render_template('deleteaccount.html')

@app.route('/deleteacc', methods =['GET', 'POST'])
def deleteacc():
    if request.method == 'POST':
        acc_number = int(request.form['acc_number'])
        is_valid_acc = Accounts.query.filter_by(acc_number=acc_number).first()
        if is_valid_acc is not None:
            Accounts.query.filter_by(acc_number=acc_number).delete()
            db.session.commit()
            flash('Account deletion initiated successfully')
        else:
            flash('No record found')
    
    return render_template('deleteaccount.html')

@app.route('/getaccountdetails', methods=['GET','POST'])
def getaccountdetails():
    return render_template('getaccdetails.html', error=False)

@app.route('/showaccounts')
def showaccounts():
    return render_template('showaccounts.html', accounts=Accounts.query.all())
    
@app.route('/customerinfo',methods=['GET','POST'])
def customerinfo():
    if request.method == 'POST':
        ssn = request.form['ssn']
        if ssn:
            print("HERRRERERERERERRE" + ssn)
            is_valid_acc = Customer.query.filter_by(ssn=ssn).first()
            if is_valid_acc is not None:
                details = Customer.query.get(ssn)
                cust = {'cust_id' : details.cust_id, 'name' : details.name, 'address' : details.address, 'age' : details.age}
                return render_template('customerinfo.html' , cust=cust)
            else:
                flash("Please enter a valid Customer ID/Account Number")
                return redirect(url_for('customerinfo'))
    return render_template('customerinfo.html', cust={})


@app.route('/accdetails', methods=['GET', 'POST'])
def accdetails():
    cust_ssn_ID = request.form['custID']
    accID = request.form['accID']
    if accID:
        accID = int(accID)
        is_valid_acc = Accounts.query.filter_by(acc_number=accID).first()
        if is_valid_acc is not None:
            details = Accounts.query.get(accID)
            data = {'acc_number' : details.acc_number, 'acc_type' : details.acc_type, 'balance' : details.balance, 'cust_id' : details.cust_id}
            return render_template('displayaccdetails.html', details=data)
    elif cust_ssn_ID:
        cust_ssn_ID = int(cust_ssn_ID)
        print("TESTED")
        is_valid_ssn = Customer.query.filter_by(ssn=cust_ssn_ID).first()
        is_valid_cust = Customer.query.filter_by(cust_id=cust_ssn_ID).first()
        print(is_valid_cust)
        if is_valid_cust is not None:
            details = Accounts.query.filter_by(cust_id=cust_ssn_ID).all()
            #print(details[0])
            data = {'acc_number' : details[0].acc_number, 'acc_type' : details[0].acc_type, 'balance' : details[0].balance, 'cust_id' : details[0].cust_id}
            return render_template('displayaccdetails.html', details=data)
        elif is_valid_ssn is not None:
            cust_details = Customer.query.get(cust_ssn_ID)
            details = Accounts.query.filter_by(cust_id=cust_details.cust_id).all()
            data = {'acc_number' : details[0].acc_number, 'acc_type' : details[0].acc_type, 'balance' : details[0].balance, 'cust_id' : details[0].cust_id}
            return render_template('displayaccdetails.html', details=data)
    else:
        flash("Please enter a valid Customer ID/Account Number")
    return render_template('getaccdetails.html', error=True)


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        amt = int(request.form['amount'])
        accID = request.form['accID']  #from displayaccdetails.html
        if accID:
            is_valid_acc = Accounts.query.filter_by(acc_number=accID).first()
            if is_valid_acc is not None:
                details = Accounts.query.get(accID)
                before_balance = details.balance
                if amt < before_balance:
                    details.balance = int(details.balance) - int(amt)
                    after_balance = details.balance
                    db.session.commit()
                    data = {'accID' : accID, 'before_balance' :before_balance, 'after_balance' : after_balance}
                    flash("Withdraw Successful")
                    return render_template('withdraw.html', data=data, flag=False)
                else:
                    flash("Please enter a valid amount")
                    return redirect(url_for('withdraw', data={}, flag=True ))
    return render_template('withdraw.html')



@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if request.method == 'POST':
        amt = int(request.form['amount'])
        source_acc = request.form['source_acc']
        dest_acc = request.form['dest_acc']
        if source_acc:
            is_valid_acc = Accounts.query.filter_by(acc_number=source_acc).first()
            if is_valid_acc is not None:
                details_src = Accounts.query.get(source_acc)
                before_balance_src = details_src.balance
                details_dest = Accounts.query.get(dest_acc)
                before_balance_dest = details_dest.balance
                if amt < before_balance_src:
                    details_src.balance = int(details_src.balance) - int(amt)
                    after_balance_src =  details_src.balance
                    details_dest.balance = int(details_dest.balance) + int(amt)
                    after_balance_dest = details_dest.balance
                    source_type = Accounts.query.filter_by(acc_number=source_acc).first().acc_type
                    target_type = Accounts.query.filter_by(acc_number=dest_acc).first().acc_type
                    tran = Transaction(cust_id=details_src.cust_id, acc_number=source_acc, source_acc_type=source_type  , target_acc_type=target_type  , amount=amt)
                    db.session.add(tran)
                    db.session.commit()
                    data = {'src_acc_no' : source_acc,'dest_acc_no' : dest_acc, 'before_balance_src' : before_balance_src, 
                    'after_balance_src' : after_balance_src, 'before_balance_dest' : before_balance_dest, 'after_balance_dest' : after_balance_dest}
                    flash('Transfer Successful!')
                    return render_template('transfer.html', data=data)
                else:
                    flash("Transfer Failed! Please enter a valid amount")
                    return redirect(url_for('transfer'))
    return render_template('transfer.html', data={})


@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        amt = int(request.form['amount'])
        accID = request.form['accID']
        if accID:
            is_valid_acc = Accounts.query.filter_by(acc_number=accID).first()
            if is_valid_acc is not None:
                details = Accounts.query.get(accID)
                before_balance = details.balance
                details.balance = int(details.balance) + int(amt)
                after_balance = details.balance
                db.session.commit()
                data = {'accID' : accID, 'before_balance' :before_balance, 'after_balance' : after_balance}
                flash('Deposit Successful')
                return render_template('deposit.html', data=data)
            else:
                flash("Please enter a valid Account Number")
                return redirect(url_for('deposit'))
    return render_template('deposit.html', data={})


@app.route('/accountstatement', methods=['GET', 'POST'])
def accountstatement():
    if request.method == 'POST':
        accID = request.form['accID']
        n = request.form['last_n']
        if accID and n:
            is_valid_acc = Accounts.query.filter_by(acc_number=accID).first()
            if is_valid_acc is not None:
                details = Transaction.query.filter_by(acc_number=accID).limit(n).all()
                acc_data = []
                for d in details:
                    x = {'acc_no': d.acc_number, 'tran_date' : d.tran_date, 'amount' : d.amount, 'source' : d.source_acc_type, 'target' : d.target_acc_type}
                    acc_data.append(x)
                return render_template('accountstatement.html', statement=acc_data)
            else:
                flash("Please enter a valid Account Number")
                return redirect(url_for('accountstatement'))
        else:
            flash("Please enter a valid details")
            return redirect(url_for('accountstatement'))
    return render_template('accountstatement.html', statement={})

