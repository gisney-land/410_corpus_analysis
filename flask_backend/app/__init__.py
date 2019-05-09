from flask import Flask
from flask_cors import CORS

def create_app(debug=True):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'
    CORS(app)

    from . import api

    app.register_blueprint(api.api_bp)

    return app
