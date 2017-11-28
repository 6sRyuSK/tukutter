from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def helloworld():
  return 'hello world!!'

@app.route('/mypage')
def mypage():
  print("!!!!!!!!!!!!この川!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  return 'nice to meet you'

@app.route('/fukai')
def fukai():
  
  name = request.args.get('name')
  return name


@app.route('/regist', methods=['POST'])
def regist():
  name = request.form['name']
  return name

@app.route('/user/<userId>')
def userpage(userId=0):
  return userId