from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


class User:
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


users = []


@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    expected_keys = ['id', 'name', 'email', 'password']
    if not all(key in data for key in expected_keys):
        return jsonify({'error': 'Missing keys in request body'}), 400
    user = User(data['id'], data['name'], data['email'], data['password'])
    users.append(user)
    return jsonify({'message': 'User added successfully'}), 201


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    users.remove(user)
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/users', methods=['GET'])
def list_users():
    return render_template('users.html', users=users)


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    return jsonify({'message': 'User updated successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
