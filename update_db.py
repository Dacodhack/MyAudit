import os
import importlib
from app import app, db
from myaudit.models import *

def record_exists(model_class, data):
    filters = {key: value for key, value in data.items() if key in ['id_chapitre', 'question']}  # Champs uniques
    return db.session.query(model_class).filter_by(**filters).first() is not None

def insert_data(model_name, data):
    model_class = globals().get(model_name)
    if not model_class:
        print(f"Modèle non trouvé : {model_name}")
        return
    # Vérification avant insertion
    if record_exists(model_class, data):
        #print(f"Le record pour {data} existe déjà, insertion ignorée.")
        return
    instance = model_class(**data)
    db.session.add(instance)

def initialize_database():
    with app.app_context():
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
