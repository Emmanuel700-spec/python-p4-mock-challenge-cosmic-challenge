from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Scientist, Planet, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Adjust database URI as needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/scientists', methods=['GET'])
def get_scientists():
    scientists = Scientist.query.all()
    return jsonify([scientist.to_dict() for scientist in scientists]), 200

@app.route('/scientists/<int:id>', methods=['GET'])
def get_scientist_by_id(id):
    scientist = Scientist.query.get(id)
    if scientist:
        return jsonify(scientist.to_dict()), 200
    return jsonify({"error": "Scientist not found"}), 404

@app.route('/scientists', methods=['POST'])
def create_scientist():
    data = request.get_json()
    try:
        scientist = Scientist(name=data['name'], field_of_study=data['field_of_study'])
        db.session.add(scientist)
        db.session.commit()
        return jsonify(scientist.to_dict()), 201
    except ValueError as e:
        return jsonify({"errors": e.args[0]}), 400

@app.route('/scientists/<int:id>', methods=['PATCH'])
def update_scientist(id):
    data = request.get_json()
    scientist = Scientist.query.get(id)
    if not scientist:
        return jsonify({"error": "Scientist not found"}), 404
    try:
        if 'name' in data:
            scientist.name = data['name']
        if 'field_of_study' in data:
            scientist.field_of_study = data['field_of_study']
        db.session.commit()
        return jsonify(scientist.to_dict()), 202
    except ValueError as e:
        return jsonify({"errors": e.args[0]}), 400

@app.route('/scientists/<int:id>', methods=['DELETE'])
def delete_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return jsonify({"error": "Scientist not found"}), 404
    db.session.delete(scientist)
    db.session.commit()
    return jsonify({}), 204

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.to_dict() for planet in planets]), 200

@app.route('/missions', methods=['POST'])
def create_mission():
    data = request.get_json()
    try:
        mission = Mission(
            name=data['name'],
            scientist_id=data['scientist_id'],
            planet_id=data['planet_id']
        )
        db.session.add(mission)
        db.session.commit()
        return jsonify(mission.to_dict()), 201
    except ValueError as e:
        return jsonify({"errors": e.args[0]}), 400

if __name__ == '__main__':
    app.run(debug=True)
