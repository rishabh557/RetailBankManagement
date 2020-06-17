from application import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user
import datetime


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class Cashier(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Cashier %r>' % self.username


class Executive(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Executive %r>' % self.username


class Accounts(db.Model):
    acc_number = db.Column(db.Integer(), primary_key=True)
    acc_type = db.Column(db.String())
    balance = db.Column(db.Integer)
    cust_id = db.Column(db.Integer, db.ForeignKey('transaction.cust_id'))

    def __init__(self, acc_number, acc_type, balance, cust_id):
        self.acc_number = acc_number
        self.acc_type = acc_type
        self.balance = balance
        self.cust_id = cust_id


class Transaction(db.Model):
    cust_id = db.Column(db.Integer, primary_key=True)
    acc_number = db.Column(db.Integer(), db.ForeignKey('accounts.acc_number'))
    source_acc_type = db.Column(db.String())
    target_acc_type = db.Column(db.String())
    tran_date = db.Column(db.DateTime, default=datetime.datetime.now)
    amount = db.Column(db.Integer)
    
    def __init__(self, cust_id, acc_number, source_acc_type, target_acc_type, amount):
        self.cust_id = cust_id
        self.acc_number = acc_number
        self.source_acc_type = source_acc_type
        self.target_acc_type = target_acc_type
        self.amount = amount


class Customer(db.Model):
    ssn = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('transaction.cust_id'))
    name = db.Column(db.String())
    address = db.Column(db.String())
    age = db.Column(db.Integer)

    def __init__(self, ssn, cust_id, name, address, age):
        self.ssn = ssn
        self.cust_id = cust_id
        self.name = name
        self.address = address
        self.age = age


db.create_all()
        