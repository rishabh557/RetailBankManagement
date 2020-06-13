from application import app
from flask import Flask, render_template, redirect, url_for

@app.route('/home')
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/home/executivelogin')
def executivelogin():
    return render_template('executivelogin.html')

@app.route('/home/cashierlogin')
def cashierlogin():
    return render_template('cashierlogin.html')
