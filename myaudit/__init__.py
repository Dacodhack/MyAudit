from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, template_folder='templates/html')
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    with app.app_context():
        from .models import Users
        from .routes import register_blueprints
        register_blueprints(app)


        upload_folder = app.config['UPLOAD_FOLDER']

        @login_manager.user_loader
        def load_user(user_id):
            return Users.query.get(int(user_id))
        
        @app.errorhandler(404)
        def not_found_error(error):
            return render_template('erreur.html', erreur="Erreur 404")

    return app
