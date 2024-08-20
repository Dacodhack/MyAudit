import os
from myaudit import create_app, db, login_manager
from config import config

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()