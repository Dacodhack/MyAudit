from myaudit import db, login_manager


from myaudit.models import Missions, MissionDroits, Domaines, Themes, Chapitres, Questions, QuestionsCache, MissionReponse, RecommendationsAudit
from myaudit.forms import MissionForm, QuestionnaireForm, AddUserToMissionForm
from myaudit.utils import log_action, check_permissions

from sqlalchemy import or_

from werkzeug.utils import secure_filename

from flask import current_app, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

import datetime, os

mission = Blueprint('mission', __name__)

@mission.route('/missions', methods=['GET', 'POST'])
@log_action
@login_required
def missions():
        missions = Missions.query.join(MissionDroits).filter(MissionDroits.id_user == current_user.id_user, MissionDroits.droit.in_(['chef de projet', 'auditeur'])).all()
        return render_template('missions.html', missions=missions)

@mission.route('/create_mission', methods=['GET', 'POST'])
@log_action
@login_required
def create_mission():
    form = MissionForm()
    domaines = Domaines.query.all()
    choices = []
    themes_dict = {}

    for domaine in domaines:
        theme = Themes.query.get(domaine.id_theme)
        if theme.id_theme not in themes_dict:
            themes_dict[theme.id_theme] = theme.theme
        choices.append((domaine.id_domaine, f"{theme.theme} - {domaine.domaine}"))

    form.id_domaine.choices = choices

    if form.validate_on_submit():
        mission = Missions(
            id_domaine=form.id_domaine.data,
            mission=form.mission.data,
            client_name=form.client_name.data,
            client_company=form.client_company.data,
            client_address=form.client_address.data,
            client_siren=form.client_siren.data,
            client_produit=form.client_produit.data,
            client_representative=form.client_representative.data,
            client_title=form.client_title.data,
            date_création=datetime.date.today(),
            date_planification=form.date_planification.data,
            date_presentation=form.date_presentation.data,
            date_restitutation=form.date_restitutation.data,
            date_debut_mission=form.date_debut_mission.data,
            date_fin_mission=form.date_fin_mission.data,
            date_debut_audit=form.date_debut_audit.data,
            date_fin_audit=form.date_fin_audit.data,
            date_rapport=form.date_rapport.data,
            date_lastUpdate=datetime.date.today()
        )
        try:
            db.session.add(mission)
            db.session.flush()
        except:
            return render_template('erreur.html', erreur="Erreur dans la création d'une mission")
        mission_droit = MissionDroits(
            id_mission=mission.id_mission,
            id_user=current_user.id_user,
            droit='chef de projet'
        )

        db.session.add(mission_droit)
        db.session.commit()

        flash('Mission created successfully!', 'success')
        return redirect(url_for('mission.missions'))

    return render_template('create_mission.html', title='Nouvelle mission', form=form)

@mission.route('/edit_mission/<int:id_mission>', methods=['GET', 'POST'])
@log_action
@login_required
@check_permissions(lambda id_mission: id_mission, required_roles=['chef de projet'])
def edit_mission(id_mission):
    mission = Missions.query.get_or_404(id_mission)
    form = MissionForm()
    domaines = Domaines.query.all()
    choices = []
    themes_dict = {}

    for domaine in domaines:
        theme = Themes.query.get(domaine.id_theme)
        if theme.id_theme not in themes_dict:
            themes_dict[theme.id_theme] = theme.theme
        choices.append((domaine.id_domaine, f"{theme.theme} - {domaine.domaine}"))

    form.id_domaine.choices = choices

    if form.validate_on_submit():
        mission.id_domaine = form.id_domaine.data
        mission.mission = form.mission.data
        mission.client_name = form.client_name.data
        mission.client_company = form.client_company.data
        mission.client_address = form.client_address.data
        mission.client_siren = form.client_siren.data
        mission.client_produit = form.client_produit.data
        mission.client_representative = form.client_representative.data
        mission.client_title = form.client_title.data
        mission.date_planification = form.date_planification.data
        mission.date_presentation = form.date_presentation.data
        mission.date_restitutation = form.date_restitutation.data
        mission.date_debut_mission = form.date_debut_mission.data
        mission.date_fin_mission = form.date_fin_mission.data
        mission.date_debut_audit = form.date_debut_audit.data
        mission.date_fin_audit = form.date_fin_audit.data
        mission.date_rapport = form.date_rapport.data
        mission.date_lastUpdate = datetime.date.today()
        db.session.add(mission)
        db.session.commit()
        flash('Domaine updated successfully', 'success')
        return redirect(url_for('mission.missions'))
    elif request.method == 'GET':
        form.mission.data = mission.mission
        form.client_name.data = mission.client_name
        form.client_company.data = mission.client_company
        form.client_address.data = str(mission.client_address)
        form.client_siren.data = str(mission.client_siren)
        form.client_produit.data = str(mission.client_produit)
        form.client_representative.data = str(mission.client_representative)
        form.client_title.data = str(mission.client_title)
        form.date_planification.data = mission.date_planification
        form.date_presentation.data = mission.date_presentation
        form.date_restitutation.data = mission.date_restitutation
        form.date_debut_mission.data = mission.date_debut_mission
        form.date_fin_mission.data = mission.date_fin_mission
        form.date_debut_audit.data = mission.date_debut_audit
        form.date_fin_audit.data = mission.date_fin_audit
        form.date_rapport.data = mission.date_rapport
    
    return render_template('edit_mission.html', title='Edition de la misson {{mission.client_name}}', form=form)

@mission.route('/edit_right/<int:id_mission>', methods=['GET', 'POST'])
@log_action
@login_required
@check_permissions(lambda id_mission: id_mission, required_roles=['chef de projet'])
def edit_right(id_mission):
    mission = Missions.query.get_or_404(id_mission)
    form = AddUserToMissionForm()
    if form.validate_on_submit():
        user_id = form.user.data
        role = form.role.data
        existing_entry = MissionDroits.query.filter_by(id_mission=id_mission, id_user=user_id).first()
        if existing_entry:
            existing_entry.droit = role
            flash('Cet utilisateur a déjà été ajouté à cette mission.', 'danger')
        else:
            new_entry = MissionDroits(id_mission=id_mission, id_user=user_id, droit=role)
            db.session.add(new_entry)
        db.session.commit()
        flash('Utilisateur ajouté avec succès à la mission.', 'success')
        return redirect(url_for('mission.missions', id_mission=id_mission))
    return render_template('edit_right.html', form=form, mission=mission)


@mission.route('/travail/<int:id_mission>', methods=['GET'])
@log_action
@login_required
@check_permissions(lambda id_mission: id_mission, required_roles=['chef de projet', 'auditeur'])
def travail(id_mission):
    if not QuestionsCache.query.filter_by(id_mission=id_mission).all():
        update_question_cache(id_mission)
    questions = QuestionsCache.query.filter_by(id_mission=id_mission).all()
    questions_list = [question.to_dict() for question in questions]
    return render_template('travail.html', title='Questions à réaliser', questions_list=questions_list)


#region Questionnaire
@mission.route('/questionnaire/<int:id_mission>/<int:id_question>', methods=['GET', 'POST'])
@log_action
@login_required
@check_permissions(lambda id_mission, id_question: id_mission, required_roles=['chef de projet', 'auditeur'])
def questionnaire(id_mission, id_question):
    questioncache = QuestionsCache.query.filter_by(id_mission=id_mission,id_question=id_question).first()
    recommendations_audit_list = RecommendationsAudit.query.filter_by(id_questionsCache=questioncache.id_questionsCache).all()
    recommendations_audit_dicts = [ra.to_dict() for ra in recommendations_audit_list]

    if request.method == 'POST':
        OLD_id_question = id_question - 1
        reponse = MissionReponse.query.filter_by(id_mission=id_mission, id_question=OLD_id_question).first()    
        question = QuestionsCache.query.filter_by(id_mission=id_mission, id_question=OLD_id_question).first()
        form = QuestionnaireForm(obj=reponse)

        if not question:
            flash('Question not found', 'danger')
            return redirect(url_for('menu.dashboard'))
        
        if form.validate_on_submit():
            filename = None
            if form.piece_jointe.data:
                filename = secure_filename(form.piece_jointe.data.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                form.piece_jointe.data.save(os.path.join(upload_folder, filename))
            
            
            if reponse:
                reponse.reponse = form.reponse.data
                reponse.evaluation = form.evaluation.data
                reponse.piece_jointe = filename
            else:
                reponse = MissionReponse(
                    id_mission=id_mission,
                    id_question=OLD_id_question, # Envoie les données de la question précédente
                    id_user=current_user.id_user,
                    reponse=form.reponse.data,
                    evaluation=form.evaluation.data,
                    piece_jointe=filename
                )
                db.session.add(reponse)
            db.session.commit()
            flash('Réponse enregistrée!', 'success')

    question = QuestionsCache.query.filter_by(id_mission=id_mission, id_question=id_question).first()
    reponse = MissionReponse.query.filter_by(id_mission=id_mission, id_question=id_question).first()
    form = QuestionnaireForm(obj=reponse)
    
    return render_template('questionnaire.html', title='Questionnaire', form=form, question=question, reponse=reponse, recommendations_audit=recommendations_audit_dicts)


def update_question_cache(id_mission):
    from datetime import datetime
    mission = Missions.query.get(id_mission)
    if not mission:
        raise ValueError(f"No mission found with id {id_mission}")
    id_domaine = mission.id_domaine
    questions = Questions.query.join(Chapitres).filter(Chapitres.id_domaine == id_domaine).all()
    for question in questions:
        existing_cache = QuestionsCache.query.filter_by(id_mission=id_mission, id_question=question.id_question).first()
        if not existing_cache:
            new_cache = QuestionsCache(id_mission=id_mission, id_question=question.id_question)
            db.session.add(new_cache)
    QuestionsCache.query.filter_by(id_mission=id_mission).update({QuestionsCache.timestamp: datetime.utcnow()})
    db.session.commit()