import os
import base64
from flask import Flask, redirect, request, send_file, Response
import minecraft_launcher_lib
app = Flask('app')

CLIENT_ID = os.environ['client_id']
SECRET = os.environ['client_secret']
REDIRECT_URL = "https://mcprox.hard-shutdown.repl.co/mcprox/processcode"


@app.route('/')
def hello_world():
  return '<h1>Hello, World! Available Routes: /mcprox</h1>'

@app.route('/mcprox')
def mcprox_main():
  return '<h1>Ok use route /getmsauth to use my server to get a microsoft auth code. After auth, you will be given a JSON responce with skin, name, uuid, access_token, refresh_token</h1>'

@app.route('/mcprox/getmsauth')  
def mcprox_msa():
  return redirect(minecraft_launcher_lib.microsoft_account.get_login_url(CLIENT_ID, REDIRECT_URL))

@app.route('/mcprox/getmsauthlocal')  
def mcprox_msaa():
  return redirect(minecraft_launcher_lib.microsoft_account.get_login_url(CLIENT_ID, REDIRECT_URL + "local"))  

@app.route('/mcprox/processcode', methods=['GET'])  
def mcprox_process():
  code = request.args.get("code")
  login_data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, SECRET, REDIRECT_URL, code)
  return '{"id": "' + login_data["id"] + '", "access_token": "' + login_data["access_token"] + '", "name": "' + login_data["name"] + '"}'                      
@app.route('/mcprox/processcodelocal', methods=['GET'])  
def mcprox_processs():
  code = request.args.get("code")
  login_data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, SECRET, REDIRECT_URL + "local", code)
  return redirect(f"http://localhost:8867/authfinish?id={login_data['id']}&access_token={login_data['access_token']}&name={login_data['name']}")

@app.route('/mcprox/getStoreInfo', methods=['GET'])
def getStoreInfo():
  return minecraft_launcher_lib.microsoft_account.get_store_information(request.args.get("token"))

@app.route('/.well-known/microsoft-identity-association.json')
def ms_verify():
  return Response("{\"associatedApplications\":[{\"applicationId\": \"94c4aa15-4917-488a-b1fd-348064d249b3\"}]}", mimetype="application/json")


app.run(host='0.0.0.0', port=8080)