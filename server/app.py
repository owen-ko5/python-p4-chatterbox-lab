from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return make_response(jsonify([m.to_dict() for m in messages]), 200)

    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_message = Message(
                body=data['body'],
                username=data['username']
            )
            db.session.add(new_message)
            db.session.commit()
            return make_response(jsonify(new_message.to_dict()), 201)
        except KeyError as e:
            return make_response(jsonify({"error": f"Missing field: {e}"}), 400)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def handle_message_by_id(id):
    message = db.session.get(Message, id)
    if not message:
        return make_response(jsonify({"error": "Message not found"}), 404)

    if request.method == 'PATCH':
        data = request.get_json()
        if 'body' in data:
            message.body = data['body']
            db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({"message": "Message deleted"}), 200)

if __name__ == '_main_':
    app.run(port=5555)
