from flask import Flask, render_template,  redirect, url_for, request, flash,json,jsonify
from flask_wtf import Form
from wtforms import StringField, BooleanField 
from wtforms.validators import DataRequired
from wtforms import BooleanField, TextField, PasswordField, validators
from wtforms.validators import Required
from forms import SignupFormdemo
import MySQLdb
from MySQLdb import escape_string as thwart
import gc
import random, itertools
WTF_CSRF_ENABLED = False
import hashlib

app = Flask(__name__)
app.secret_key = 'adbmssecretkey'

def pidgenerator():
	conn = connection()
	cursor=conn.cursor()
	sql = "SELECT max(pid) FROM passenger"
	cursor.execute(sql)
	result=cursor.fetchall()
	r=int(result[0][0])	
	nextpid=r+1
	return nextpid
	cursor.close()
	conn.close()
	
	
def connection():
    conn = MySQLdb.connect(host="localhost",user = "root",passwd = "root",db = "metrodb")
    
    return conn
	
	
@app.route("/")
def main():    
	return render_template('main.html')


@app.route("/logout")
def logout():    
	return render_template('main.html')


	
@app.route("/success",methods=['GET','POST'])
def success():    
	return render_template('success.html')
	
@app.route("/checkpnr",methods=['GET','POST'])
def checkpnr():    
	return render_template('checkpnr.html')
	
@app.route("/error")
def error():    
	return render_template('error.html')
	
@app.route("/btnhome",methods=['GET','POST'])
def btnhome():
	if request.form['btn'] == "s":
		return redirect(url_for('check'))
	elif request.form['btn'] == "p":
		return redirect(url_for('checkpnr'))
	elif request.form['btn'] == "b":
		return redirect(url_for('booking'))
	else:
		return redirect(url_for('error'))
		

@app.route("/pnrstatus",methods=['GET','POST'])
def pnrstatus():    
	error=''
	try:		
		pnr=request.form['pnr']
		#pnr=int(pnrget)
		print(pnr)
		conn = connection()
		cursor=conn.cursor()
		x=cursor.execute("SELECT pnr,concat(fname,' ',lname) as passengername, age,gender,traveldate ,tsource,TDESTINATION,ARRTIME,DEPTIME FROM metrodb.passenger ,metrodb.ticket,metrodb.train ,metrodb.ttime where passenger.PID=ticket.pid and ticket.ROUTEID=ttime.ROUTEID and ttime.TRAIN_ID=train.TRAINID and ticket.pnr=(%s)",[pnr])
		#cursor.execute(sql)
		if int(x) > 0:
			result=cursor.fetchall()
			cursor.close()
			conn.close()
			return render_template("pnrstatus.html",result=result)
			gc.collect()
		else:
			flash("Please enter a valid ticket id")
			error ="Please enter a valid ticket id"
			conn.commit()
			cursor.close()
			conn.close()
			return render_template("error.html",errir=error)
	except Exception(e):
		flash(e)
		return render_template("homepage.html", error = error)  
	
@app.route("/booking",methods=['GET','POST'])
def booking():    
	error=''
	try:		
		conn = connection()
		cursor=conn.cursor()
		sql = "SELECT curdate() ,tsource,TDESTINATION,ARRTIME,DEPTIME,fare FROM metrodb.ticket,metrodb.train ,metrodb.ttime,metrodb.fare where ticket.ROUTEID=ttime.ROUTEID and ttime.TRAIN_ID=train.TRAINID and ticket.ROUTEID=fare.ROUTEID;"
		cursor.execute(sql)
		result=cursor.fetchall()
		cursor.close()
		conn.close()
		return render_template("booking.html",result=result)
		gc.collect()
	except Exception(e):
		flash(e)
		return render_template("homepage.html", error = error)  
	



	
@app.route("/check",methods=['GET','POST'])
def check():
	error=''
	try:		
		conn = connection()
		cursor=conn.cursor()
		sql = "SELECT curdate() ,tsource,TDESTINATION,ARRTIME,DEPTIME,fare,running_status FROM metrodb.ticket,metrodb.train ,metrodb.ttime,metrodb.fare where ticket.ROUTEID=ttime.ROUTEID and ttime.TRAIN_ID=train.TRAINID and ticket.ROUTEID=fare.ROUTEID;"
		cursor.execute(sql)
		result=cursor.fetchall()
		cursor.close()
		conn.close()
		return render_template("check.html",result=result)
		gc.collect()
	except Exception(e):
		flash(e)
		return render_template("homepage.html", error = error)  
	
	

@app.route('/signUpUser',methods=['GET','POST'])
def signUpUser():
	error=''
	try:
		
		if request.method == 'POST':
			fname = request.form.get('first_name')
			lname = request.form.get('last_name')
			email = request.form['email']
			user_id = request.form.get('user_name')
			user_password = request.form['password']
			age = request.form.get('age')
			gender = request.form['gender']
			phone = request.form['contact_no']
			cardholdername=request.form['cardholdername']
			cardnumber=request.form['cardnumber']
			expiry_month=request.form['expiry_month']
			expiry_year=request.form['expiry_year']
			cardcvv=request.form['cardcvv']
			conn = connection()
			c=conn.cursor()
			x = c.execute("SELECT * FROM PASSENGER WHERE USER_ID = (%s)",[user_id])
			if int(x) > 0:
				flash("That username is already taken, please choose another")
				error ="That username is already taken, please choose another"
				conn.commit()
				c.close()
				conn.close()
				return render_template("signup.html",error=error)
			else:
				h = hashlib.md5(user_password.encode())
				pswd=h.hexdigest()
				pid=pidgenerator()
				c.execute("""INSERT INTO passenger (  PID,user_id,user_password, fname, lname, age, gender,email,phone,card_holder_name,card_number,card_exp_month,card_exp_year,card_cvv)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", ( pid, user_id,pswd, fname, lname, age, gender,email,phone,cardholdername,cardnumber,expiry_month,expiry_year,cardcvv))
				conn.commit()
				flash("Thanks for registering!")
				c.close()
				conn.close()
				gc.collect()
				return redirect(url_for('homepage'))
			
		else:
			flash("Method not POST")
			return render_template("signup.html",error=error)
		
	except Exception(e):
		flash(e)
		return render_template("signup.html", error = error)  



@app.route("/signup/",methods=['GET','POST'])
def signup():
	try:
		return render_template('signup.html')
	except Exception as e:
		flash(e)
		return render_template("main.html", error = error)

	
@app.route("/homepage/",methods=['GET','POST'])
def homepage():
	return render_template('homepage.html')  


@app.route("/loginpage/",methods=['GET'])
def loginpage():
	return render_template('login.html')  

	
@app.route("/login/",methods=['GET','POST'])
def login():
	error = None
	conn = connection()
	c=conn.cursor()
	user_id=request.form['user_name']
	password=request.form['password']
	h = hashlib.md5(password.encode())
	x = c.execute("SELECT * FROM PASSENGER WHERE USER_ID = (%s)",[user_id])
	r=c.rowcount	
	if r == 0:
		flash("Invalid Username, Please try again")
		error ="Invalid Username, Please try again"
		conn.commit()
		c.close()
		conn.close()
		return render_template("login.html",error=error)
	else:
		data = c.fetchone()[2]
		if data==h.hexdigest(): 
			conn.commit()
			c.close()
			conn.close()
			return redirect(url_for('homepage'))
		else:
			flash("Invalid Password")
			conn.commit()
			c.close()
			conn.close()
			return render_template("login.html",error=error)

if __name__ == "__main__":
	app.run()