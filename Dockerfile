# Utiliser une image de base avec Python
FROM python:3.10-slim

# Installer gcc et d'autres dépendances nécessaires pour la compilation
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*



# Définir le répertoire de travail dans le conteneur
WORKDIR /myaudit

# Copier les fichiers de l'application dans le conteneur
COPY . /myaudit

# Installer les dépendances de l'application
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application va tourner
EXPOSE 5000

# Définir la commande pour lancer l'application
CMD ["flask", "run", "--host=0.0.0.0"]
