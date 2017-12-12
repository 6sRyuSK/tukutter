import MySQLdb
from flask import Flask, render_template, request, redirect, make_response
import hashlib

application = Flask(__name__)

def dbcon(sql, args):
  db = MySQLdb.connect( user='root', passwd='root', host='localhost', db='tukutter', charset='utf8' )
  con = db.cursor()

  # sql = 'SELECT user_pass from users where login_id = %s'
  con.execute(sql, args)
  db.commit()
  result = con.fetchall()
  #DBの切断
  db.close()
  con.close()
  return result

def logcheck():
  user_id = request.cookies.get('user_id', None)
  user_pass = request.cookies.get('user_pass', None)
  if user_id and user_pass is not None:
    sql = 'SELECT user_pass, login_id, user_name from users where id = %s'
    args = [user_id]
    result = dbcon(sql, args)
    login_id = result[0][1]
    user_name = result[0][2]
    if user_pass == result[0][0]:
      return [True, user_id, login_id, user_name]
  else:
    return render_template('login.html')

@application.route('/')
def top():
  log = logcheck()
  if log[0] is not True:
    return log  #template login_html

  login_user_id = log[1]
  sql = "SELECT users.user_name, content, tubuyaki.post_time FROM tubuyaki inner join users on tubuyaki.user_id = users.id inner join follow on tubuyaki.user_id = follow.follow_id where follow.user_id = %s and delete_flg = 0 ORDER BY tubuyaki.id DESC"
  args = [login_user_id]
  result = dbcon(sql, args)
  return render_template('timeline.html', rows=result)

@application.route('/search')
def search():
  search_query = "%"+request.args.get('search_query')+"%"
  if search_query is not None:
    sql = "SELECT users.user_name, content, tubuyaki.post_time FROM tubuyaki inner join users on tubuyaki.user_id = users.id where delete_flg = 0 and content LIKE %s ORDER BY tubuyaki.id DESC"
    args = [search_query]
    result = dbcon(sql, args)
    return render_template('timeline.html', rows=result)
  return redirect('/')

@application.route('/tweet', methods=['POST'])
def tweet():
  tweet = request.form['tweet']
  log = logcheck()
  if log[0] is not True:
    return log  #template login_html
  sql = 'INSERT into tubuyaki(user_id, content) value (%s, %s)'
  args = [log[1], tweet]
  result = dbcon(sql, args)
  return redirect('/')

@application.route('/user/<user_id>')
def user_prof():
  

  return "user_profile" + user_id


@application.route('/tubuyaki/<tubuyaki_id>')
def tubuyaki_show():
  return "tubuyki"

@application.route('/login')
def login_form():
  
  log = logcheck()
  if log[0] is True:
    return log[1] + "でログイン中です。"
  return log  #template login_html

@application.route('/login', methods=['POST'])
def login():
  
  login_id = request.form['login_id']
  user_pass = request.form['user_pass']
  hashstring = hashlib.md5(user_pass.encode('utf-8')).hexdigest()

  sql = 'SELECT user_pass from users where login_id = %s'
  args = [login_id]
  result = dbcon(sql, args)

  if hashstring == result[0][0]:
    sql = 'SELECT id from users where login_id = %s'
    args = [login_id]
    result = dbcon(sql, args)
    user_id = str(result[0][0])
    response = make_response(redirect('/'))
    response.set_cookie('user_id', user_id)
    response.set_cookie('user_pass', hashstring)
    print(login_id)
    return response

  return "not login"


@application.route('/register')
def register_form():
  return render_template('register.html')

@application.route('/register', methods=['POST'])
def register():
  
  login_id = request.form['login_id']
  user_name = request.form['user_name']
  user_pass = request.form['user_pass']
  hashstring = hashlib.md5(user_pass.encode('utf-8')).hexdigest()

  

  sql = 'SELECT login_id from users where login_id = %s'
  args = [login_id]
  result = dbcon(sql, args)
  if result is ():
    response = make_response(redirect('/'))
    sql = 'INSERT into users(login_id, user_name, user_pass) value (%s, %s, %s)'
    args = [login_id, user_name, hashstring]
    result = dbcon(sql, args)
    sql = 'SELECT id from users where login_id = %s'
    args = [login_id]
    result = dbcon(sql, args)
    user_id = str(result[0][0])
    response.set_cookie('user_id', user_id)
    response.set_cookie('user_pass', hashstring)
    return response
  return render_template('register.html', error=1)
  

  
  