import os
import yaml
import subprocess
from sqlalchemy.exc import SQLAlchemyError
from app import app, db
from myaudit.models import Recommendations

def clone_repository(repo_url, destination):
    try:
        if os.path.exists(destination):
            print(f"Le répertoire {destination} existe déjà.")
        else:
            subprocess.run(["git", "clone", repo_url, destination], check=True)
            print(f"Clonage du dépôt {repo_url} terminé dans {destination}.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du clonage du dépôt : {e}")
        raise

def load_yaml_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"): 
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                try:
                    documents = yaml.safe_load_all(file)
                    for data in documents:
                        if data:
                            insert_recommendation(data)
                except yaml.YAMLError as e:
                    print(f"Erreur lors de la lecture du fichier {filename}: {e}")

def insert_recommendation(data):
    try:
        recommendation = ''.join(map(str, data.get('description', []))) if data.get('description') else None
        vulnerability = ''.join(map(str, data.get('vulnerability', []))) if data.get('vulnerability') else None
        impact = ''.join(map(str, data.get('Impact', []))) if data.get('Impact') else None
        probability = ''.join(map(str, data.get('Probability', []))) if data.get('Probability') else None
        referents = ''.join(data.get('referents', [])) if data.get('referents') else None
        livrables = ''.join(data.get('livrables', [])) if data.get('livrables') else None
        sources = ''.join(data.get('sources', [])) if data.get('sources') else None

        recommendation = Recommendations(
            titre_reco=data.get('recommandation', ''),
            recommendation=recommendation,
            titre_vuln=data.get('TVuln', ''),
            vuln=vulnerability,
            v_impact=impact,
            v_proba=probability,
            referents=referents,
            livrables=livrables,
            sources=sources
        )
        db.session.add(recommendation)
        db.session.commit()
        print(f"Recommandation insérée: {recommendation.recommendation}")
    except SQLAlchemyError as e:
        db.session.rollback()  # Annuler la transaction en cas d'erreur
        print(f"Erreur lors de l'insertion dans la base de données: {e}")

if __name__ == "__main__":
    repo_url = "git@github.com:Dacodhack/Adrela.git"
    destination = os.path.join(os.getcwd(), "Adrela")

    try:

        clone_repository(repo_url, destination)

    except:
        print(f"Erreur lors du clonage")
    
    try:
        directory = os.path.join(destination, "_adrela")
        with app.app_context():
            load_yaml_files(directory)
    except:
        print(f"Erreur lors de l'import")
