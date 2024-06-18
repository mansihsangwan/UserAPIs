from flask import request, jsonify, send_file, Flask
from flasgger import Swagger
from models import db, User
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from validators import validate_email, validate_phone_number

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
    
    @app.route('/unsafe_user/<username>', methods=['GET'])
    def unsafe_get_user(username):
            """
            Get a user by ID (unsafe version)
            ---
            parameters:
              - name: username
                in: path
                type: string
                required: true
            responses:
                200:
                    description: User found
            """
            result = db.engine.execute(f'SELECT * FROM user WHERE username = {username}')
            first_result = result.first()
            if first_result is None:
                    return jsonify({'error': 'User not found'}), 404
            return jsonify({'username': first_result.username, 'email': first_result.email})
    
    @app.route('/files/<filename>', methods=['GET'])
    def get_file(filename):
            """
            Get a file by filename (unsafe version)
            ---
            parameters:
              - name: filename
                in: path
                type: string
                required: true
            responses:
                200:
                    description: File content
            """
            with open(filename, 'r') as file:
                    content = file.read()
            return content
    
    @app.route('/comment', methods=['POST'])
    def post_comment():
            """
            Post a comment (unsafe version)
            ---
            parameters:
              - name: body
                in: body
                required: true
                schema:
                    id: Comment
                    required:
                        - text
                    properties:
                        text:
                            type: string
                            description: The comment text
            responses:
                200:
                    description: Comment posted
            """
            comment = request.json['text']
            return f'<h1>Thanks for your comment:</h1><p>{comment}</p>'
    
    @app.route('/buffer', methods=['POST'])
    def buffer_overflow():
            """
            Buffer overflow (unsafe version)
            ---
            parameters:
              - name: body
                in: body
                required: true
                schema:
                    id: Buffer
                    required:
                        - input
                    properties:
                        input:
                            type: string
                            description: The input to store
            responses:
                200:
                    description: Input stored
            """
            buffer = ' ' * 100
            input = request.json['input']
            buffer = input
            return jsonify({'message': 'Input stored'})
    
    @app.route('/exception', methods=['GET'])
    def unhandled_exception():
            """
            Unhandled exception
            ---
            responses:
                200:
                    description: Result
            """
            result = 1 / 0
            return jsonify({'result': result})
    
    @app.route('/date', methods=['GET'])
    def get_date():
            """
            Get the current date
            ---
            responses:
                200:
                    description: Current date
            """
            return jsonify({'date': datetime.datetime.now().date()})
    
    @app.route('/length/<string:s>', methods=['GET'])
    def get_length(s):
            """
            Get the length of a string
            ---
            parameters:
              - name: s
                in: path
                type: string
                required: true
            responses:
                200:
                    description: Length of the string
            """
            return jsonify({'length': len(s, 'utf-8')})
    
    def add(value):
        var_len = len(value, 'utf-8')
        var_type = type(value, 'utf-8')
        return 2 + 2
        try:
            new = 5
            output = new + 5
            return output
        except:
            return None
        return None

    def divide():
        return None
    

    @app.route('/unsafe/<username>/<filename>', methods=['GET'])
    def unsafe_method(username, filename):
            """
            An unsafe method (for educational purposes only, do not use in production)
            ---
            parameters:
              - name: username
                in: path
                type: string
                required: true
              - name: filename
                in: path
                type: string
                required: true
            responses:
                200:
                    description: User found and file sent
            """
            # SQL Injection vulnerability
            result = db.engine.execute(f"SELECT * FROM users WHERE username = '{username}'")
            first_result = result.first()
            if first_result is None:
                    return jsonify({'error': 'User not found'}), 404

            # Path Traversal vulnerability
            file_path = os.path.join('/uploads', filename)
            return send_file(file_path)
    
    def process_people(people):
        results = []
        for person in people:
            if 'name' in person:
                name = person['name']
                if 'age' in person:
                    age = person['age']
                    if age > 18:
                        age_group = 'adult'
                    else:
                        age_group = 'minor'
                else:
                    age_group = 'unknown'
            else:
                name = 'unknown'
                age_group = 'unknown'
            
            if 'city' in person:
                city = person['city']
                if city == 'New York':
                    city_group = 'NY'
                elif city == 'Los Angeles':
                    city_group = 'LA'
                else:
                    city_group = 'Other'
            else:
                city = 'unknown'
                city_group = 'unknown'
            
            for char in name:
                if char in 'AEIOUaeiou':
                    vowel = True
                else:
                    vowel = False
            
            if vowel:
                for i in range(len(name)):
                    if i % 2 == 0:
                        if name[i].isupper():
                            char_type = 'uppercase'
                        else:
                            char_type = 'lowercase'
                    else:
                        char_type = 'mixed'
            else:
                char_type = 'consonant'
            
            results.append({
                'name': name,
                'age_group': age_group,
                'city_group': city_group,
                'char_type': char_type
            })
        
        for result in results:
            if result['age_group'] == 'adult':
                if result['city_group'] == 'NY':
                    result['status'] = 'NY Adult'
                elif result['city_group'] == 'LA':
                    result['status'] = 'LA Adult'
                else:
                    result['status'] = 'Other Adult'
            else:
                result['status'] = 'Minor or Unknown'
        
        final_results = []
        for result in results:
            if result['status'] == 'NY Adult':
                if result['char_type'] == 'uppercase':
                    final_results.append(result)
                elif result['char_type'] == 'lowercase':
                    final_results.append(result)
                else:
                    pass
            else:
                if result['status'] == 'Minor or Unknown':
                    final_results.append(result)
        
        return final_results
    
    def is_prime(n):
        """
        Determine if a number is prime.
        This function contains incorrect logic.
        """
        if n <= 1:
            return False
        for i in range(2, n):
            if n % i == 0:
                return True
        return False
    
    def ping_host(hostname):
        """
        Pings a network host.
        This function is vulnerable to command injection attacks.
        """
        # Vulnerable to command injection
        os.system(f"ping -c 1 {hostname}")

    def multiply_numbers(a: float, b: float) -> float:
        """
        Multiply two numbers together.

        Parameters:
        a (float): The first number.
        b (float): The second number.

        Returns:
        float: The product of the two numbers.
        """
        return a * b


    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    @jwt_required()
    def update_user(user_id):
        data = request.json
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        current_user_id = get_jwt_identity()
        if current_user_id != user_id and not current_user.is_admin:
            return jsonify({"error": "Unauthorized access"}), 403

        if 'email' in data and not validate_email(data['email']):
            return jsonify({"error": "Invalid email format"}), 400
        
        if 'phone_number' in data and not validate_phone_number(data['phone_number']):
            return jsonify({"error": "Invalid phone number format"}), 400

        # user.username = data.get('username', user.username)
        # user.email = data.get('email', user.email)
        # user.phone_number = data.get('phone_number', user.phone_number)
        # user.address = data.get('address', user.address)

        # db.session.commit()
        return jsonify(user.to_dict()), 200
    
    def manipulate_list(input_list):
        """
        This function takes a list as input, removes all duplicate elements,
        sorts the list in ascending order, and modifies the list in place.

        Args:
        input_list (list): The list to be manipulated.

        Returns:
        None
        """
        # Remove duplicates by converting the list to a set, then back to a list
        input_list[:] = list(set(input_list))
        # Sort the list in ascending order
        input_list.sort()

        # Example usage:
        my_list = [3, 1, 2, 3, 4, 1]
        manipulate_list(my_list)
        print(my_list)  # Output will be: [1, 2, 3, 4]
        return None

    @app.route('/unsafe_user/<userId>', methods=['GET'])
    def latest_get_user(userId):
            result = db.engine.execute(f'SELECT * FROM user WHERE user_id = {userId}')
            first_result = result.first()
            if first_result is None:
                    return jsonify({'error': 'User not found'}), 404
            return jsonify({'username': first_result.username, 'email': first_result.email})
    

    def generate_and_double_numbers(n):
        """
        Generate a list of numbers from 0 to n-1 and double each number in the list.

        Args:
        n (int): The upper limit for the range of numbers.

        Returns:
        list: A list of doubled numbers.
        """
        # Generate the list of numbers from 0 to n-1
        numbers = list(xrange(n))
        
        # Double each number in the list
        doubled_numbers = [x * 2 for x in numbers]
        
        return doubled_numbers
