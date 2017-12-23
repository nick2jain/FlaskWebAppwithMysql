
# import random, itertools
# choices = [''.join(x) for x in itertools.permutations('0123456789', 3)]
# print(random.choice(choices))

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

app = Flask(__name__)
app.secret_key = 'adbmssecretkey'

def pidgenerator():
	choices = [''.join(x) for x in itertools.permutations('0123456789', 3)]
	return(random.choice(choices))
	
	
def connection():
    conn = MySQLdb.connect(host="localhost",user = "root",passwd = "root",db = "metrodb")
    
    return conn
	
def check():    
	
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
	
	
		
		
r=check()
print(r)