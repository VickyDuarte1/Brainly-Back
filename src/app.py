from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/users', methods=['POST'])
def createUser():
  print(request.json)
#  id = db.insert({})
  return jsonify()


@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    # for doc in db.find():
    #     users.append({
    #     })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
#  user = db.find_one({'_id': ObjectId(id)})
  return jsonify()


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
#  db.delete_one({'_id': ObjectId(id)})
  return jsonify({'message': 'User Deleted'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
  print(request.json)
#  db.update_one({'_id': ObjectId(id)}, {"$set": {
#    'name': request.json['name'],
#   'email': request.json['email'],
#  'password': request.json['password']
#}})
  return jsonify({'message': 'User Updated'})

if __name__ == '__main__':
    app.run(debug=True)