from flask import Flask, jsonify,  request, abort
from flask_cors import CORS, cross_origin

from .models import setup_db, Plant
import os

def create_app(test_config=None):
    
    app = Flask(__name__)
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        setup_db(app)
    app.config.from_mapping(
        SECRET_KEY='dev', 
        DATABASE=os.path.join(app.instance_path, 'flask-api.sqlite'),
    )

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Autorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, PATCH, DELETE, OPTIONS')
        return response

    @cross_origin()
    @app.route('/')
    def index():
        return jsonify(
                {"msg": 'hey hey heeeey'}
                )

    @app.route('/plants', methods=['GET', 'POST'])
    def plants():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        plants = Plant.query.all()
        formatted_data = [plant.format() for plant in plants]

        return jsonify(
            {
                "status": True,
                "plants" : formatted_data[start:end],
                "plants_count": len(formatted_data)
            }
        )

    @app.route('/plants/<int:plant_id>')
    def get_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)
        else:

            return jsonify(
                {
                    "success": True,
                    "Plant": plant.format()
                }
            )

    return app