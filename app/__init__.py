from flask import Flask
from app.extensions import db, jwt, migrate

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db) 

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.purchase_routes import purchase_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(purchase_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
