import MySQLdb
from flask import Flask, render_template, request, redirect, make_response

application = Flask(__name__)

@application.route('/')
def top():
  # db = MySQLdb.connect( user='root', passwd='root', host='localhost', db='myapp', charset='utf8' )
  # con = db.cursor()

  # sql = 'SELECT content from tubuyaki

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
  db = MySQLdb.connect( user='root', passwd='root', host='localhost', db='myapp', charset='utf8' )
  con = db.cursor()
  return None


@application.route('/register', methods=['POST'])
def register():
  
  # #mysqlに接続する
  # db = MySQLdb.connect( user='root', passwd='root', host='localhost', db='myapp', charset='utf8')
  # con = db.cursor()

  # #取得したタスクの内容をtodoテーブルに追加する
  # sql = 'insert into users(login_id) value (%s)'
  # con.execute(sql,[task])
  # db.commit()

  # #DBの切断
  # db.close()
  # con.close()

  # #新規追加が終わったら、一覧画面へジャンプする
  return redirect('http://localhost/')