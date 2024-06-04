from flask import request, jsonify
from flasgger import Swagger
from models import db, User
import os

def init_app(app):
    Swagger(app)
    @app.route('/users', methods=['POST'])
    def create_user():
        """
        Create a new user
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: User
              required:
                - username
                - email
              properties:
                username:
                  type: string
                  description: The user's name
                email:
                  type: string
                  description: The user's email
        responses:
          201:
            description: User created
        """
        username = request.json['username']
        email = request.json['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({'username': user.username, 'email': user.email}), 201

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        """
        Get a user by ID
        ---
        parameters:
          - name: user_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: User found
        """
        user = User.query.get(user_id)
        return jsonify({'username': user.username, 'email': user.email})

    @app.route('/run', methods=['POST'])
    def run_command():
        """
        Run a command
        ---
        parameters:
          - name: command
            in: formData
            type: string
            required: true
        responses:
          200:
            description: Command output
        """
        command = request.form['command']
        return os.popen(command).read()
    
    @app.route('/complex', methods=['GET'])
    def complex_method():
        """
        A complex method
        ---
        responses:
          200:
            description: Method executed
        """
        result = 0
        for i in range(100):
            for j in range(100):
                for k in range(100):
                    if i == j and j == k:
                        result += 1
                    elif i != j and j != k:
                        result -= 1
                    else:
                        result = 0
        return jsonify({'result': result})
    
    @app.route('/buggy', methods=['POST'])
    def buggy_endpoint():
        """
        A buggy endpoint
        ---
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: Buggy
              properties:
                key:
                  type: string
                  description: A key
        responses:
          200:
            description: Key value
        """
        key = request.json["key"]
        return jsonify({'value': data['non_existent_key']})
        json_data = jsonify({'value': data['non_existent_key']})
        return json_data
    
    @app.route('/unsafe_user/<user_id>', methods=['GET'])
    def unsafe_get_user(user_id):
            """
            Get a user by ID (unsafe version)
            ---
            parameters:
              - name: user_id
                in: path
                type: string
                required: true
            responses:
                200:
                    description: User found
            """
            result = db.engine.execute(f'SELECT * FROM user WHERE id = {user_id}')
            first_result = result.first()
            if first_result is None:
                    return jsonify({'error': 'User not found'}), 404
            return jsonify({'username': first_result.username, 'email': first_result.email})