from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)

# app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = 'mongodb://localhost/pythontest.users'

mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def create_user():    
    name = request.json['name']
    lastname = request.json['lastname']
    username = request.json['username']
    email = request.json['email']
    

    if name and lastname and  username and email:
        
        id = mongo.db.users.insert(
            {name:'name',lastname:'lastname','username': username, 'email': email, })
        response = jsonify({
            '_id': str(id),
            'name': name,
            'lastname':lastname,
            'username':username,           
            'email': email
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    print(username)
    user = mongo.db.users.find_one({'_username': ObjectId(username), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)