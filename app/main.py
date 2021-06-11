from flask import Flask, request, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Leaderboards.db'
db  = SQLAlchemy(app)

class Users(db.Model):
   user_id = db.Column(db.Integer,primary_key=True, nullable=False)
   username = db.Column(db.String(150), default="")
   mins = db.Column(db.Integer, default=0)

   def __repr__(self):
     return '<User %s>' %self.username

db.create_all()

@app.route("/")
def hello():
  return "<h1>Welcome to Leaderboards API</h1>"

@app.route('/addtime', methods=['POST']) 
def index():
  if request.method == 'POST':
    record = json.loads(request.data)
    dcid = record["discordID"]
    dcname = record["username"]
    dcmins = record["mins"]
    print("98")
    new_user = Users.query.get(dcid)
    print("99")    
    if new_user == None:
      new_user = Users(user_id=dcid, username=dcname, mins=dcmins)
      print("1")
      try:
          db.session.add(new_user)
          db.session.commit()
          return jsonify("New User added")
      except:
          return jsonify("Issue adding the user")
    else:
      print("2")
      k = new_user.mins
      print("3")
      new_user.mins = k + dcmins
      print("4")
      try:
        db.session.commit()
        return jsonify("Updated the user")
      except:
        return jsonify("Failed to update the user"+new_user.username)        



@app.route('/getleaderboard',methods=["GET"])
def getData():
   
      Leaderboards = Users.query.order_by(Users.mins).all()
      empty_arr = []
      for user in Leaderboards:
        empty_arr.append({
          "discordID": user.user_id,
          "username": user.username,
          "mins": math.floor(user.mins/60000)
        })
      return jsonify(empty_arr)
   
      # return jsonify("Couldnt get the data")


