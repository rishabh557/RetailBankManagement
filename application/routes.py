from application import app
from flask import render_template
from .models import Cashier, Executive, Accounts, db, Transaction, Customer, login_manager, login_required, login_user, SQLAlchemy
from flask import Flask, render_template, redirect, url_for, request


@app.route('/home')
@app.route("/")
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
def executivecashier():
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
