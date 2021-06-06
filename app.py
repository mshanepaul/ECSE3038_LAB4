rom flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from keys import keys
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = keys["uri"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
mrsh = Marshmallow(app)
dte = datetime.datetime.now()

profileDB = {
  
    "sucess": True,
    "data": {
        "last_updated": "2/3/2021, 8:48:51 PM",
        "username": "user1",
        "role": "Engineer",
        "color": "red"
    }
}

class Tank(db.Model):
  __tablename__ = 'tanks'

  id = db.Column(db.Integer, primary_key = True)
  location = db.Column(db.String(), nullable=False)
  lat = db.Column(db.Float(), nullable=False)
  long = db.Column(db.Float(), nullable=False)
  percentage_full = db.Column(db.Integer(), nullable=False)

class TankSchema(mrsh.SQLAlchemySchema):
  class Meta:
    model = Tank
    fields = ("id", "location", "lat", "long", "percentage_full")

db.init_app(app) 
migrate = Migrate(app, db)

@app.route("/", methods=["GET"])
def home():
    return "hello lab 3"

# PROFILE Routes:
@app.route("/profile", methods=["GET", "POST", "PATCH"])
def profile():
    if request.method == "POST":
        # /POST
        profileDB["data"]["last_updated"] = (dte.strftime("%c"))
        profileDB["data"]["username"] = (request.json["username"])
        profileDB["data"]["role"] = (request.json["role"])
        profileDB["data"]["color"] = (request.json["color"])
       
        return jsonify(profileDB)
   
    elif request.method == "PATCH":
        # /PATCH
        profileDB["data"]["last_updated"] = (dte.strftime("%c"))
        
        tempDict = request.json
        attributes = tempDict.keys()
        
        for attribute in attributes:
            profileDB["data"][attribute] = tempDict[attribute]
  
        return jsonify(profileDB)

    else:
        # /GET
        return jsonify(profileDB)

# DATA Routes:
@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        # /POST
        newTank = Tank(
            location = request.json["location"],
            lat =  request.json["lat"],
            long = request.json["long"],
            percentage_full = request.json["percentage_full"]
        )

        db.session.add(newTank)
        db.session.commit()
        return TankSchema().dump(newTank)

    else:
        # /GET

        tanks = Tank.query.all()
        tanks_json = TankSchema(many=True).dump(tanks)
        return  jsonify(tanks_json)


@app.route("/data/<int:id>", methods=["PATCH", "DELETE"])
def update(id):

    if request.method == "PATCH":
        # /PATCH
        
        tank = Tank.query.get(id)
        update = request.json

        if "location" in update: tank.location = update["location"]
        if "lat" in update: tank.lat = update["lat"]
        if "long" in update: tank.long = update["long"]
        if "percentage_full" in update: tank.percentage_full = update["percentage_full"]
        
        db.session.commit()
        return TankSchema().dump(tank)     
        
       

    elif request.method == "DELETE":
        # /DELETE

        tank = Tank.query.get(id)
        
        db.session.delete(tank)
        db.session.commit()
        return {"success": True}

    else:
        # /GET

        tanks = Tank.query.all()
        tanks_json = TankSchema(many=True).dump(tanks)
        return  jsonify(tanks_json)

# Main
if __name__ == '__main__':
   app.run(debug = True)
