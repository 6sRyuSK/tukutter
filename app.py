import MySQLdb
from flask import Flask, render_template, request, redirect, make_response
import hashlib

application = Flask(__name__)

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
  return "login"

@application.route('/login', methods=['POST'])
def login():
  db = MySQLdb.connect( user='root', passwd='root', host='localhost', db='tukutter', charset='utf8' )
  con = db.cursor()
  return None


@application.route('/register')
def register_form():
  return render_template('register.html')

@application.route('/register', methods=['POST'])
def register():
  
  login_id = request.form['login_id']
  user_name = request.form['user_name']
  user_pass = request.form['user_pass']
  hashstring = hashlib.md5(user_pass.encode('utf-8')).hexdigest()

  #mysqlに接続する
  db = MySQLdb.connect( user='root', passwd='root', host='localhost', db='tukutter', charset='utf8')
  con = db.cursor()

  sql = 'insert into users(login_id, user_name, user_pass) value (%s, %s, %s)'
  con.execute(sql,[login_id, user_name, hashstring])
  db.commit()

  #DBの切断
  db.close()
  con.close()

  # #新規追加が終わったら、一覧画面へジャンプする
  return redirect('http://localhost/')