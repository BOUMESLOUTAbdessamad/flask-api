from flask import Flask, jsonify
from flask_cors import CORS

import os

def create_app(test_config=None):
    
    app = Flask(__name__)
    cors = CORS(app, resources={r'*/api/*': {origins: '*'}})

    app.config.from_mapping(
        SECRET_KEY='dev', 
        DATABASE=os.path.join(app.instance_path, 'flask-api.sqlite'),
    )


    @app.route('/')
    def index():
        return jsonify(
                {"msg": 'hey hey heeeey'}
                )
    @app.route('/restaurents')
    def get_restaurents():
        return jsonify(
            {
                "1": "Bahia",
                "2" : "Oran"
            }
        )
    return app


