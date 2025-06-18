from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
CORS(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200

class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {'error': 'Plant not found'}, 404
        return plant.to_dict(), 200
    
    def patch(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {'error': 'Plant not found'}, 404

        data = request.get_json()
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']
            db.session.commit()
        return plant.to_dict(), 200

    def delete(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {'error': 'Plant not found'}, 404

        db.session.delete(plant)
        db.session.commit()
        return '', 204

# Routes
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

