import os
import importlib
from app import app, db
from myaudit.models import *

def insert_data(model_name, data):
    """Insère les données dans la base de données pour un modèle donné."""
    model_class = globals().get(model_name)
    if not model_class:
        print(f"Modèle non trouvé : {model_name}")
        return

    instance = model_class(**data)
    db.session.add(instance)

def initialize_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        init_db_directory = 'init_db'
        for filename in os.listdir(init_db_directory):
            if filename.endswith('.py'):
                module_name = f"init_db.{filename[:-3]}"
                module = importlib.import_module(module_name)

                if hasattr(module, 'get_data'):
                    data_list = module.get_data()
                    for item in data_list:
                        insert_data(item['model'], item['data'])

        db.session.commit()

if __name__ == "__main__":
    initialize_database()
