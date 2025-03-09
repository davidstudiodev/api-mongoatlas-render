from flask import Flask, jsonify, request
from dotenv import load_dotenv
from bson import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import os

load_dotenv()

app = Flask(__name__)

uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.shopify
users = db.users

@app.route('/read', methods=['GET'])
def read():
    
    listUsers = list(users.find())
    
    for user in listUsers:
        user['_id'] = str(user['_id'])
    
    return jsonify({'Users': listUsers})

@app.route('/add', methods=['POST'])
def add():
    
    data = request.json
    
    newUser = {
        'name': data['name'],
        'age': data['age']
    }
    
    users.insert_one(newUser)
    
    return jsonify({'Message': 'User added'})

@app.route('/update/<string:id>', methods=['PUT'])
def update(id):
    
    data = request.json
    
    newUser = {
        'name': data['name'],
        'age': data['age']
    }
    
    query = users.update_one({'_id': ObjectId(id)}, {'$set': newUser})
    
    if query.modified_count > 0:
        return jsonify({'Message': 'User updated'})

@app.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
    
    query = users.delete_one({'_id': ObjectId(id)})
    
    if query.deleted_count > 0:
        return jsonify({'Message': 'User deleted'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)

