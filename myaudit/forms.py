from myaudit import db
from myaudit.models import Users

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField, FileField, DateField
from wtforms.validators import DataRequired, Regexp, Email, Length, EqualTo, ValidationError

from datetime import datetime, timedelta
class LoginForm(FlaskForm):
    username = StringField('Pseudonyme', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Pseudonyme', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enregistrer')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class ThemeForm(FlaskForm):
    theme = StringField('Theme:', validators=[DataRequired()])
    submit = SubmitField('Enregistrer le thème')


class DomaineForm(FlaskForm):
    id_theme = SelectField('Thème Id', validators=[DataRequired()], coerce=int, choices=[])
    domaine = StringField('Domaine:', validators=[DataRequired()])
    submit = SubmitField('Enregistrer le domaine')

class ChapitreForm(FlaskForm):
    id_domaine = SelectField('Domaine Id', validators=[DataRequired()], coerce=int, choices=[])
    chapitre = StringField('Chapitre:', validators=[DataRequired()])
    submit = SubmitField('Enregistrer le chapitre')

class QuestionForm(FlaskForm):
    id_chapitre = SelectField('Chapitre', coerce=int, validators=[DataRequired()])
    question = StringField('Question', validators=[DataRequired()])
    objectif = StringField('Objectif', validators=[DataRequired()])
    submit = SubmitField('Enregistrer la question')

class RecommandationForm(FlaskForm):
    recommandation = StringField('Recommandation:', validators=[DataRequired()])

    id_recommandation = db.Column(db.Integer, primary_key=True)
    titre_reco = StringField('Titre de la recommandation:', validators=[DataRequired()])
    recommandation = StringField('Recommandation:', validators=[DataRequired()])
    titre_vuln = StringField('Titre de la vulnérabilité:', validators=[DataRequired()])
    vuln = StringField('Vulnérabilité:', validators=[DataRequired()])
    v_impact = SelectField('Évaluation', choices=[
        ('0', 'Mineur'),
        ('1', 'Significatif'),
        ('2', 'Grave'),
        ('3', 'Critique'),
        ('4', 'Catastrophique')
    ], default='0')
    v_proba = SelectField('Évaluation', choices=[
        ('0', 'Invraisemblable'),
        ('1', 'Peu vraisemblable'),
        ('2', 'Vraisemblable'),
        ('3', 'Très vraisemblable'),
        ('4', 'Quasi certain')
    ], default='0')
    submit = SubmitField('Enregistrer la recommandation')


class MissionForm(FlaskForm):
    id_domaine = SelectField('Domaine', validators=[DataRequired()], choices=[])
    mission = StringField('Nom de la mission:', validators=[DataRequired()], default='Mission Fantôme')
    client_name = StringField('Nom du client', validators=[DataRequired()], default='David Perez')
    client_company = StringField("Nom de l'entreprise",  default='Dacodhack')
    client_address = StringField('Adresse',  default='1 Grand Rue, 34000 Montpellier')
    client_siren = StringField('Siren', validators=[Regexp('^\d+$', message="Le SIREN doit être un nombre composé de chiffres")], default='922793989')
    client_produit = StringField('Produit audité',  default="Adrela")
    client_representative = StringField('Représentant',  default="David Perez")
    client_title = StringField('Titre du Représentant',  default="RSSI")
    date_planification = DateField('Date de planification' , default=datetime.today() )
    date_presentation = DateField('Date de presentation' , default=datetime.today()+ timedelta(days=2) )
    date_restitutation = DateField('Date de restitutation' , default=datetime.today()+ timedelta(days=25) )
    date_debut_mission = DateField('Date de debut_mission' , default=datetime.today()+ timedelta(days=25) )
    date_fin_mission = DateField('Date de fin de la mission' , default=datetime.today()+ timedelta(days=2) )
    date_debut_audit = DateField('Date de debut de l\'audit' , default=datetime.today()+ timedelta(days=5) )
    date_fin_audit = DateField('Date de fin de la audit' , default=datetime.today()+ timedelta(days=20) )
    date_rapport = DateField('Date de rapport' , default=datetime.today()+ timedelta(days=20) )
    submit = SubmitField('Créer la mission')

class QuestionnaireForm(FlaskForm):
    reponse = TextAreaField('Réponse', validators=[DataRequired()])
    evaluation = SelectField('Évaluation', choices=[
        ('0', 'Mesure à ignorer'),
        ('1', 'Mesure non évaluable'),
        ('2', 'Mesure inexistante'),
        ('3', 'Mesure en cours de réflexion'),
        ('4', 'Mesure en cours d’implémentation'),
        ('5', 'Mesure implémentée'),
        ('6', 'Mesure implémentée avec procédures associées')
    ], default='0')
    piece_jointe = FileField('Pièce jointe', validators=[FileAllowed(['jpg', 'png', 'pdf', 'doc', 'docx'], 'Files only!')])
    submit = SubmitField('Valider')

class MissionDroitForm(FlaskForm):
    id_user = SelectField('Users', coerce=int, validators=[DataRequired()])
    droit = SelectField('Droit', choices=[('chef de projet', 'Chef de projet'), ('auditeur', 'Auditeur')], validators=[DataRequired()])
    submit = SubmitField('Enregistrer les droits')


class AddUserToMissionForm(FlaskForm):
    user = SelectField('Utilisateur', validators=[DataRequired()], choices=[])
    role = SelectField('Rôle', validators=[DataRequired()], choices=[
        ('chef de projet', 'Chef de projet'),
        ('auditeur', 'Auditeur'),
        ('desactivé', 'Supprimer')
    ])
    submit = SubmitField('Ajouter')

    def __init__(self, *args, **kwargs):
        super(AddUserToMissionForm, self).__init__(*args, **kwargs)
        self.user.choices = [(user.id_user, user.username) for user in Users.query.all()]
