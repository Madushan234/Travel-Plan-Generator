from flask import Flask
from .routes import travel_plan_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(travel_plan_bp)

    return app
