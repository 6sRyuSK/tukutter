from flask import Flask, request
application = Flask(__name__)

@application.route('/')
def helloworld():
  return 'hello world!!'

@application.route('/mypage')
def mypage():
  print("!!!!!!!!!!!!この川!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  return 'nice to meet you'

@application.route('/fukai')
def fukai():
  
  name = request.args.get('name')
  return name


@application.route('/regist', methods=['POST'])
def regist():
  name = request.form['name']
  return name

@application.route('/user/<userId>')
def userpage(userId=0):
  return userId