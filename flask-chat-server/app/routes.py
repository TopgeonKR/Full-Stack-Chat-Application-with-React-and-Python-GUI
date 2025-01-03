from flask import Blueprint, jsonify, request, session
from flask_socketio import emit
from .models import User, Chat, db
from . import socketio

main = Blueprint('main', __name__)

# Register
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    new_user = User(username=username, password_hash=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 200


# Login
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.password_hash == password:
        session['username'] = username  # 세션에 사용자 이름 저장
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid username or password."}), 401




# Reset Password
@main.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    new_password = data.get('new_password')

    if not username or not password or not new_password:
        return jsonify({"error": "All fields are required."}), 400

    user = User.query.filter_by(username=username).first()
    if not user or user.password_hash != password:
        return jsonify({"error": "Invalid username or password."}), 401

    user.password_hash = new_password
    db.session.commit()
    return jsonify({"message": "Password reset successful!"}), 200


# Delete User
@main.route('/delete-user', methods=['POST'])
def delete_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if not user or user.password_hash != password:
        return jsonify({"error": "Invalid username or password."}), 401

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200


# User List
@main.route('/userlist', methods=['GET'])
def userlist():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify({"users": user_list}), 200

# chat
@main.route('/chat', methods=['GET'])
def chat():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    username = session['username']
    messages = Chat.query.order_by(Chat.timestamp).all()
    chat_history = [{"username": msg.username, "message": msg.message, "timestamp": msg.timestamp} for msg in messages]

    return jsonify({"username": username, "messages": chat_history}), 200




# WebSocket: Handle new messages
@socketio.on('send_message')
def handle_send_message(data):
    username = data.get('username', 'Anonymous')
    message = data.get('message', '')

    # Save the message in the database
    new_chat = Chat(username=username, message=message)
    db.session.add(new_chat)
    db.session.commit()

    # Broadcast the message to all connected clients
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)

