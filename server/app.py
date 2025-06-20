from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Message  # assuming Message model is correctly defined

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([message.to_dict() for message in messages]), 200

# Create a new message
@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    if not data or not data.get('body') or not data.get('username'):
        return jsonify({"error": "Invalid input"}), 400

    message = Message(body=data['body'], username=data['username'])
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

# Update a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    data = request.get_json()
    message.body = data.get('body', message.body)
    db.session.commit()
    return jsonify(message.to_dict()), 200

# Delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    db.session.delete(message)
    db.session.commit()
    return '', 204
