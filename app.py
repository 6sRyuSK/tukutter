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
  login_id = request.cookies.get('login_id', None)
  user_pass = request.cookies.get('user_pass', None)
  if login_id and user_pass is not None:
    sql = 'SELECT user_pass from users where login_id = %s'
    args = [login_id]
    result = dbcon(sql, args)
    if user_pass == result[0][0]:
      return [True, login_id, user_pass]
  else:
    return render_template('login.html')

@application.route('/')
def top():
  db = MySQLdb.connect( user='root', passwd='root', host='localhost', db='tukutter', charset='utf8' )
  con = db.cursor()


  login_user_id = 2 #とりあえずjiroでログイン
  sql = "SELECT users.user_name, content FROM tubuyaki inner join users on tubuyaki.user_id = users.id inner join follow on tubuyaki.user_id = follow.follow_id where follow.user_id = %s"
  con.execute(sql,[login_user_id])

  #値を2次元配列で取得。
  result = con.fetchall()

  #DBの切断
  db.close()
  con.close()

  #一覧のデータをtimeline.htmlに渡して、ループで表示させる
  return render_template('timeline.html', rows=result)

  return "top page"

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
    response = make_response(redirect('http://localhost/'))
    max_age = 60 * 60 * 24 * 120 # 120 days
    expires = max_age
    response.set_cookie('login_id', login_id)
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

  response = make_response(redirect('http://localhost/'))
  max_age = 60 * 60 * 24 * 120 # 120 days
  expires = max_age
  response.set_cookie('login_id', login_id)
  response.set_cookie('user_pass', hashstring)


  sql = 'insert into users(login_id, user_name, user_pass) value (%s, %s, %s)'
  args = [login_id, user_name, hashstring]
  result = dbcon(sql, args)

  # #新規追加が終わったら、一覧画面へジャンプする
  return response