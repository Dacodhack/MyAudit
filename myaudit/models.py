from datetime import datetime
from flask_login import UserMixin
from myaudit import db

class Users(UserMixin, db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    droits_generaux = db.Column(db.String(20))

    def __repr__(self):
        return f"User('{self.username}')"

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id_user)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        if self.droits_generaux == "admin":
            return True

    def has_role(self, role, id_mission):
        mission_droit = MissionDroits.query.filter_by(id_user=self.id_user, id_mission=id_mission, droit=role).first()
        return mission_droit is not None

class Themes(db.Model):
    id_theme = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id_theme': self.id_theme,
            'theme': self.theme
        }

class Domaines(db.Model):
    id_domaine = db.Column(db.Integer, primary_key=True)
    domaine = db.Column(db.String(255), nullable=False)

    id_theme = db.Column(db.Integer, db.ForeignKey('themes.id_theme'), nullable=False)
    themes = db.relationship('Themes', backref='domaines', lazy=True)

    def to_dict(self):
        return {
            'id_domaine': self.id_domaine,
            'domaine': self.domaine,
            'id_theme': self.id_theme
        }

class Chapitres(db.Model):
    id_chapitre = db.Column(db.Integer, primary_key=True)
    chapitre = db.Column(db.String(255), nullable=False)

    id_domaine = db.Column(db.Integer, db.ForeignKey('domaines.id_domaine'), nullable=False)

    domaines = db.relationship('Domaines', backref='chapitres', lazy=True)

    def to_dict(self):
        return {
            'id_chapitre': self.id_chapitre,
            'chapitre': self.chapitre,
            'id_domaine': self.id_domaine
        }

#region Questions
class Questions(db.Model):
    id_question = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    objectif = db.Column(db.Text)

    id_chapitre = db.Column(db.Integer, db.ForeignKey('chapitres.id_chapitre'), nullable=False)

    chapitres = db.relationship('Chapitres', backref='questions', lazy=True)

    def to_dict(self):
        return {
            'id_question': self.id_question,
            'question': self.question,
            'objectif': self.objectif,
            'id_chapitre': self.id_chapitre
        }

class QuestionsCache(db.Model):
    __tablename__ = 'QuestionsCache'
    id_questionsCache = db.Column(db.Integer, primary_key=True)
    id_mission = db.Column(db.Integer, db.ForeignKey('missions.id_mission'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('questions.id_question'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    missions = db.relationship('Missions', backref=db.backref('questionsCache', lazy=True))
    questions = db.relationship('Questions', backref=db.backref('questionsCache', lazy=True))

    def to_dict(self):
        return {
            'id_questionsCache': self.id_questionsCache,
            'id_mission' : self.id_mission,
            'id_domaine' : self.missions.domaines.id_domaine,
            'id_chapitre' : self.questions.chapitres.id_chapitre,
            'id_question' : self.id_question,
            'mission' : self.missions.mission,
            'domaine' : self.missions.domaines.domaine,
            'chapitre' : self.questions.chapitres.chapitre,
            'question' : self.questions.question,
            'objectif' : self.questions.objectif
        }

#region Recommandations
class Recommandations(db.Model):
    __tablename__ = 'Recommandations'
    id_recommandation = db.Column(db.Integer, primary_key=True)

    titre_reco = db.Column(db.String(255), nullable=True)
    recommandation = db.Column(db.String(2550), nullable=True)

    r_prio = db.Column(db.Integer, nullable=True)

    titre_vuln = db.Column(db.String(255), nullable=True)
    vuln = db.Column(db.String(2550), nullable=True)

    v_impact = db.Column(db.Integer, nullable=True)
    v_proba = db.Column(db.Integer, nullable=True)

    referents = db.Column(db.String(255), nullable=True)
    livrables = db.Column(db.String(255), nullable=True)
    sources = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id_recommandation': self.id_recommandation,
            'titre_reco': self.titre_reco,
            'recommandation': self.recommandation,
            'r_prio': self.r_prio,
            'titre_vuln': self.titre_vuln,
            'vuln': self.vuln,
            'v_impact': self.v_impact,
            'v_proba': self.v_proba,
            'referents': self.referents,
            'livrables': self.livrables,
            'sources': self.sources
        }

class RecommandationsAudit(db.Model):
    __tablename__ = 'RecommandationsAudit'
    id_recommandationsAudit = db.Column(db.Integer, primary_key=True)
    id_recommandation = db.Column(db.Integer, db.ForeignKey('Recommandations.id_recommandation'), nullable=False)
    id_questionsCache = db.Column(db.Integer, db.ForeignKey('QuestionsCache.id_questionsCache'), nullable=False)

    recommandation = db.relationship('Recommandations', backref='RecommandationsAudit', lazy=True)
    questions_cache = db.relationship('QuestionsCache', backref='RecommandationsAudit', lazy=True)

    def to_dict(self):
        return {
            'id_recommandationsAudit': self.id_recommandationsAudit,
            'id_recommandation': self.id_recommandation,
            'id_questionsCache': self.id_questionsCache,
            'titre_reco': self.recommandation.titre_reco,
            'recommandation': self.recommandation.recommandation,
            'r_prio': self.recommandation.r_prio,
            'titre_vuln': self.recommandation.titre_vuln,
            'vuln': self.recommandation.vuln,
            'v_impact': self.recommandation.v_impact,
            'v_proba': self.recommandation.v_proba,
            'referents': self.recommandation.referents,
            'livrables': self.recommandation.livrables,
            'sources': self.recommandation.sources
        }


#region Missions
class Missions(db.Model):
    id_mission = db.Column(db.Integer, primary_key=True)
    id_domaine = db.Column(db.Integer, db.ForeignKey('domaines.id_domaine'), nullable=False)
    mission = db.Column(db.String(255), nullable=False)
    client_name = db.Column(db.String(255))
    client_company = db.Column(db.String(255))
    client_address = db.Column(db.String(255))
    client_siren = db.Column(db.String(255))
    client_produit = db.Column(db.String(255))
    client_representative = db.Column(db.String(255))
    client_title = db.Column(db.String(255))
    date_création = db.Column(db.Date, nullable=False)
    date_planification = db.Column(db.Date)
    date_presentation = db.Column(db.Date)
    date_restitutation = db.Column(db.Date)
    date_debut_mission = db.Column(db.Date)
    date_fin_mission = db.Column(db.Date)
    date_debut_audit = db.Column(db.Date)
    date_fin_audit = db.Column(db.Date)
    date_rapport = db.Column(db.Date)
    date_lastUpdate = db.Column(db.Date, nullable=False)

    domaines = db.relationship('Domaines', backref=db.backref('missions', lazy=True))

    def to_dict(self):
        return {
            'id_mission': self.id_mission,
            'id_domaine': self.domaines.id_domaine,
            'mission': self.mission,
            'client_name' : self.client_name,
            'client_company' : self.client_company,
            'client_address' : self.client_address,
            'client_siren' : self.client_siren,
            'client_produit' : self.client_produit,
            'client_representative' : self.client_representative,
            'client_title' : self.client_title,
            'date_création' : self.date_création.strftime("%Y-%m-%d"),
            'date_planification' : self.date_planification.strftime("%Y-%m-%d"),
            'date_presentation' : self.date_presentation.strftime("%Y-%m-%d"),
            'date_restitutation' : self.date_restitutation.strftime("%Y-%m-%d"),
            'date_debut_mission' : self.date_debut_mission.strftime("%Y-%m-%d"),
            'date_fin_mission' : self.date_fin_mission.strftime("%Y-%m-%d"),
            'date_debut_audit' : self.date_debut_audit.strftime("%Y-%m-%d"),
            'date_fin_audit' : self.date_fin_audit.strftime("%Y-%m-%d"),
            'date_rapport' : self.date_rapport.strftime("%Y-%m-%d"),
            'date_lastUpdate' : self.date_lastUpdate.strftime("%Y-%m-%d")
        }


class MissionDroits(db.Model):
    id_missionDroit = db.Column(db.Integer, primary_key=True)
    id_mission = db.Column(db.Integer, db.ForeignKey('missions.id_mission'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    droit = db.Column(db.String(100), nullable=False)

    missions = db.relationship('Missions', backref=db.backref('MissionDroits', lazy=True))
    users = db.relationship('Users', backref=db.backref('MissionDroits', lazy=True))

    def to_dict(self):
        return {
            'id_mission' : self.id_mission,
            'id_user' : self.id_user,
            'users' : self.users.username,
            'droit' : self.droit
        }

class MissionReponse(db.Model):
    id_missionsReponse = db.Column(db.Integer, primary_key=True)
    id_mission = db.Column(db.Integer, db.ForeignKey('missions.id_mission'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('questions.id_question'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    reponse = db.Column(db.Text)
    evaluation = db.Column(db.Integer, nullable=False)
    piece_jointe = db.Column(db.String(255))

    questions = db.relationship('Questions', backref=db.backref('missionsReponse', lazy=True))
    missions = db.relationship('Missions', backref=db.backref('missionsReponse', lazy=True))
    users = db.relationship('Users', backref=db.backref('missionsReponse', lazy=True))

    def to_dict(self):
        return {
            'id_missionReponse': self.id_missionsReponse,
            'id_mission': self.id_mission,
            'id_question': self.id_question,
            'question': self.questions.question,
            'objectif': self.questions.objectif,
            'id_chapitre': self.questions.chapitres.id_chapitre,
            'chapitre': self.questions.chapitres.chapitre,
            'réponse': self.reponse,
            'evaluation': self.evaluation,
            'piece_jointe': self.piece_jointe
        }

class MissionPieceJointe(db.Model):
    id_missionPieceJointe = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)

#region Logs
class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    url = db.Column(db.String(255))
    sended = db.Column(db.String(2550))

    def __init__(self, user, url, sended):
        self.user = user
        self.url = url
        self.sended = sended

    def to_dict(self):
        return {
            'id' : self.id,
            'user' : self.user,
            'timestamp' : self.timestamp,
            'url' : self.url,
            'sended' : self.sended
        }