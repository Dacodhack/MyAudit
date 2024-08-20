from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_user, logout_user, current_user, login_required

from myaudit import db, login_manager
from myaudit.models import Themes, Domaines, Chapitres, Questions, Recommendations
from myaudit.forms import MissionForm, ThemeForm, DomaineForm, ChapitreForm, QuestionForm, RecommendationForm
from myaudit.utils import log_action

param = Blueprint('param', __name__)

@param.route('/paramétrages', methods=['GET'])
@log_action
@login_required
def paramétrages():
    return render_template('paramétrages.html', title='Configuration de la plateforme')

#region Thème
@param.route('/create_theme', methods=['GET', 'POST'])
@log_action
@login_required
def create_theme():
    form = ThemeForm()
    if form.validate_on_submit():
        theme = Themes(theme=form.theme.data)
        db.session.add(theme)
        db.session.commit()
        flash('Thème créé avec succès', 'success')
        return redirect(url_for('param.list_themes'))
    return render_template('create_theme.html', title='Nouveau Thème', form=form)

@param.route('/list_themes', methods=['GET', 'POST'])
@log_action
@login_required
def list_themes():
    return render_template('liste_themes.html', title='Thèmes')

#region Domaine
@param.route('/create_domaine', methods=['GET', 'POST'])
@log_action
@login_required
def create_domaine():
    form = DomaineForm()
    themes = Themes.query.all()
    form.id_theme.choices = [(theme.id_theme, theme.theme) for theme in themes]

    if form.validate_on_submit():
        domaine = Domaines(id_theme=form.id_theme.data, domaine=form.domaine.data)
        db.session.add(domaine)
        db.session.commit()
        flash('Domaine créé avec succès', 'success')
        return redirect(url_for('param.list_domaines'))
    return render_template('create_domaine.html', title='Nouveau Domaine', form=form)

@param.route('/list_domaines', methods=['GET', 'POST'])
@log_action
@login_required
def list_domaines():
    return render_template('liste_domaines.html', title='Listes des thèmes')


#region Chapitre
@param.route('/create_chapitre', methods=['GET', 'POST'])
@log_action
@login_required
def create_chapitre():
    form = ChapitreForm()
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
        chapitre = Chapitres(id_domaine=form.id_domaine.data, chapitre=form.chapitre.data)
        db.session.add(chapitre)
        db.session.commit()
        flash('Chapitre créé avec succès', 'success')
        return redirect(url_for('param.list_chapitres'))
    
    return render_template('create_chapitre.html', title='Nouveau chapitre', form=form)

@param.route('/list_chapitres', methods=['GET', 'POST'])
@log_action
@login_required
def list_chapitres():
    return render_template('liste_chapitres.html', title='Listes des chapitres')

#region Question

@param.route('/create_question', methods=['GET', 'POST'])
@log_action
@login_required
def create_question():
    form = QuestionForm()
    chapitres = Chapitres.query.join(Domaines, Domaines.id_domaine == Chapitres.id_domaine).join(Themes, Themes.id_theme == Domaines.id_theme).add_columns(Themes.id_theme.label('id_theme'), Themes.theme.label('theme_texte'), Domaines.id_domaine.label('id_domaine'), Domaines.domaine.label('domaine_texte'), Chapitres.id_chapitre.label('id_chapitre'), Chapitres.chapitre.label('chapitre_texte')).all()
    chapitre_choices = [(chapitre.id_chapitre, f"{chapitre.theme_texte} - {chapitre.domaine_texte} - {chapitre.chapitre_texte}") for chapitre in chapitres]
    form.id_chapitre.choices = chapitre_choices

    if form.validate_on_submit():
        question = Questions(question=form.question.data, objectif=form.objectif.data, id_chapitre=form.id_chapitre.data)
        db.session.add(question)
        db.session.commit()
        flash('Question created successfully', 'success')
        return redirect(url_for('param.list_questions'))
    return render_template('create_question.html', title='Nouvelle question', form=form)

@param.route('/list_questions', methods=['GET', 'POST'])
@log_action
@login_required
def list_questions():
    return render_template('liste_questions.html', title='Liste des questions')

#region Recommendation
@param.route('/create_recommendation', methods=['GET', 'POST'])
@log_action
@login_required
def create_recommendation():
    form = RecommendationForm()
    if form.validate_on_submit():
        recommendation = Recommendations(
            titre_reco=form.titre_reco.data,
            recommendation=form.recommendation.data,
            r_prio=int(form.v_impact.data) * int(form.v_proba.data),
            titre_vuln=form.titre_vuln.data,
            vuln=form.vuln.data,
            v_impact=int(form.v_impact.data),
            v_proba=int(form.v_proba.data),
            )
        db.session.add(recommendation)
        db.session.commit()
        flash('Thème créé avec succès', 'success')
        return redirect(url_for('param.list_recommendations'))
    return render_template('create_recommendation.html', title='Nouvelle Recommendation', form=form)

@param.route('/list_recommendations', methods=['GET', 'POST'])
@log_action
@login_required
def list_recommendations():
    return render_template('liste_recommendations.html', title='Thèmes')