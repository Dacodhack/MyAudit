from myaudit import db, login_manager
from myaudit.models import Themes, Domaines, Chapitres, Questions, Recommandations, Missions, MissionReponse, MissionDroits, QuestionsCache, RecommandationsAudit, Logs
from myaudit.utils import log_action, check_permissions

from flask import Blueprint, flash, jsonify, render_template
from flask_login import current_user, login_user, logout_user, login_required

api = Blueprint('api', __name__)
#region API
@api.route('/api/themes', methods=['GET'])
@log_action
@login_required
def get_themes():
    themes = Themes.query.all()
    themes_list = [theme.to_dict() for theme in themes]
    return jsonify(themes_list)

@api.route('/api/theme/<int:id_theme>', methods=['GET'])
@log_action
@login_required
def get_theme(id_theme):
    themes = Themes.query.filter_by(id_theme=id_theme).all()
    themes_list = [theme.to_dict() for theme in themes]
    return jsonify(themes_list)

@api.route('/api/domaines', methods=['GET'])
@log_action
@login_required
def get_domaines():
    domaines = Domaines.query.all()
    domaines_list = [domaine.to_dict() for domaine in domaines]
    return jsonify(domaines_list)

@api.route('/api/domaine/<int:id_theme>', methods=['GET'])
@log_action
@login_required
def get_domaines_by_theme(id_theme):
    domaines = Domaines.query.filter_by(id_theme=id_theme).all()
    domaines_list = [domaine.to_dict() for domaine in domaines]
    return jsonify(domaines_list)

@api.route('/api/chapitres', methods=['GET'])
@log_action
@login_required
def get_chapitres():
    chapitres = Chapitres.query.all()
    chapitres_list = [chapitre.to_dict() for chapitre in chapitres]
    return jsonify(chapitres_list)

@api.route('/api/chapitre/<int:id_domaine>', methods=['GET'])
@log_action
@login_required
def get_chapitres_by_domaine(id_domaine):
    chapitres = Chapitres.query.filter_by(id_domaine=id_domaine).all()
    chapitres_list = [chapitre.to_dict() for chapitre in chapitres]
    return jsonify(chapitres_list)

@api.route('/api/questions', methods=['GET'])
@log_action
@login_required
def get_questions():
    questions = Questions.query.all()
    questions_list = [question.to_dict() for question in questions]
    return jsonify(questions_list)

@api.route('/api/question/<int:id_chapitre>', methods=['GET'])
@log_action
@login_required
def get_questions_by_chapitre(id_chapitre):
    questions = Questions.query.filter_by(id_chapitre=id_chapitre).all()
    questions_list = [question.to_dict() for question in questions]
    return jsonify(questions_list)

@api.route('/api/recommandations', methods=['GET'])
@log_action
@login_required
def get_recommandations():
    recommandations = Recommandations.query.all()
    recommandations_list = [recommandation.to_dict() for recommandation in recommandations]
    return jsonify(recommandations_list)

@api.route('/api/missions', methods=['GET'])
@log_action
@login_required
def get_missions():
    missions = Missions.query.all()
    missions_list = [mission.to_dict() for mission in missions]
    return jsonify(missions_list)

@api.route('/api/mission_right', methods=['GET'])
@log_action
@login_required
def get_mission_rights():
    mission_rights = MissionDroits.query.all()
    mission_rights_list = [mission_right.to_dict() for mission_right in mission_rights]
    return jsonify(mission_rights_list)

@api.route('/api/réponses', methods=['GET'])
@log_action
@login_required
def get_réponses():
    if not current_user.is_admin():
        flash('Accès refusé.', 'danger')
        return render_template('erreur.html', erreur="Seuls les administrateurs peuvent voir cette entrée API.")
    réponses = MissionReponse.query.all()
    réponses_list = [réponse.to_dict() for réponse in réponses]
    return jsonify(réponses_list)

@api.route('/api/réponse/<int:id_mission>', methods=['GET'])
@log_action
@login_required
@check_permissions(lambda id_mission: id_mission, required_roles=['chef de projet', 'auditeur'])
def get_réponses_by_mission(id_mission):
    réponses = MissionReponse.query.filter_by(id_mission=id_mission).all()
    réponses_list = [réponse.to_dict() for réponse in réponses]
    return jsonify(réponses_list)

@api.route('/api/log/', methods=['GET'])
@api.route('/api/logs/', methods=['GET'])
@log_action
@login_required
def get_logs():
    if not current_user.is_admin():
        flash('Accès refusé.', 'danger')
        return render_template('erreur.html', erreur="Seuls les administrateurs peuvent voir le journal d'événement.")
    logs = Logs.query.all()
    logs_list = [log.to_dict() for log in logs]
    return jsonify(logs_list)


@api.route('/api/recodaudit', methods=['GET'])
@log_action
@login_required
def get_list_recommandations():
    recommandations_audit_list = RecommandationsAudit.query.all()
    recommandations_audit_dicts = [ra.to_dict() for ra in recommandations_audit_list]
    return jsonify(recommandations_audit_dicts)


@api.route('/api/list/recodaudit/<int:id_mission>/<int:id_question>', methods=['GET'])
@log_action
@login_required
@check_permissions(lambda id_mission, id_question: id_mission, required_roles=['chef de projet', 'auditeur'])
def get_list_recommandation(id_mission, id_question):
    questioncache = QuestionsCache.query.filter_by(id_mission=id_mission,id_question=id_question).first()
    recommandations_audit_list = RecommandationsAudit.query.filter_by(id_questionsCache=questioncache.id_questionsCache).all()
    recommandations_audit_dicts = [ra.to_dict() for ra in recommandations_audit_list]
    return jsonify(recommandations_audit_dicts)

@api.route('/api/ajout/recodaudit/<int:id_mission>/<int:id_question>/<int:id_recommandation>', methods=['GET', 'POST'])
@log_action
@login_required
@check_permissions(lambda id_mission, id_question, id_recommandation: id_mission , required_roles=['chef de projet', 'auditeur'])
def ajout_recommandation(id_mission, id_question, id_recommandation):
    try:

        questioncache = QuestionsCache.query.filter_by(id_mission=id_mission,id_question=id_question).first()
        recommandation = RecommandationsAudit.query.filter_by(id_questionsCache=questioncache.id_questionsCache).all()
        

        recodaudit = RecommandationsAudit(
            id_recommandation=id_recommandation,
            id_questionsCache=questioncache.id_questionsCache
        )

        db.session.add(recodaudit)
        db.session.commit()
    except:
        return render_template('erreur.html', erreur="Erreur ajout 404")
    return render_template('erreur.html', erreur="Ok")


@api.route('/api/del/recodaudit/<int:id_mission>/<int:id_recommandationsAudit>', methods=['GET', 'POST'])
@log_action
@login_required
@check_permissions(lambda id_mission, id_recommandationsAudit: id_mission , required_roles=['chef de projet', 'auditeur'])
def del_recommandation(id_mission, id_recommandationsAudit):
    try:
        recommandation_audit = RecommandationsAudit.query.filter_by(id_recommandationsAudit=id_recommandationsAudit).first()
        
        if recommandation_audit:
            db.session.delete(recommandation_audit)
            db.session.commit()
            return jsonify({"success": True, "message": "RecommandationAudit supprimée avec succès."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Erreur lors de la suppression: " + str(e)}), 500
    return jsonify({"success": False, "message": "RecommandationAudit introuvable."}), 404
 
