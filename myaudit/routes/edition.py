from myaudit import db, login_manager


from myaudit.models import Missions, MissionDroits, Domaines, Themes, Chapitres, Questions, QuestionsCache, MissionReponse
from myaudit.forms import ThemeForm, MissionForm, QuestionnaireForm, AddUserToMissionForm
from myaudit.utils import log_action, check_permissions

from sqlalchemy import or_

from werkzeug.utils import secure_filename

from flask import current_app, Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required

import datetime, os

edition = Blueprint('edition', __name__)

@edition.route('/edit/theme/<int:id_theme>', methods=['GET', 'POST'])
@log_action
@login_required
def edit_theme(id_theme):
    theme = Themes.query.get_or_404(id_theme)
    form = ThemeForm()

    if form.validate_on_submit():
        theme.theme = form.theme.data
        db.session.commit()
        flash('Theme updated successfully', 'success')
        return redirect(url_for('list_themes'))

    elif request.method == 'GET':
        form.theme.data = theme.theme

    return render_template('edit_theme.html', title='Edit Theme', form=form)

@edition.route('/edit/domaine/<int:id_domaine>', methods=['GET', 'POST'])
@log_action
@login_required
def edit_domaine(id_domaine):
    domaine = Domaine.query.get_or_404(id_domaine)
    form = DomaineForm()

    themes = Theme.query.all()

    theme_choices = [(theme.id_theme, f"{theme.texte}") for theme in themes]
    form.id_theme.choices = theme_choices

    if form.validate_on_submit():
        domaine.texte = form.texte.data
        domaine.id_theme = form.id_theme.data
        db.session.commit()
        flash('Domaine updated successfully', 'success')
        return redirect(url_for('list_domaines'))

    elif request.method == 'GET':
        form.id_theme.data = domaine.id_theme
        form.texte.data = domaine.texte

    return render_template('edit_domaine.html', title='Edit Domaine', form=form)


@edition.route('/edit/chapitre/<int:id>', methods=['GET', 'POST'])
@log_action
@login_required
def edit_chapitre(id):
    chapitre = Chapitre.query.get_or_404(id)
    form = ChapitreForm()
    domaines = Domaine.query.join(Theme, Theme.id == Domaine.id_theme).add_columns(
        Theme.id_theme.label('id_theme'),
        Theme.texte.label('theme_texte'),
        Domaine.id_domaine.label('id_domaine'),
        Domaine.texte.label('domaine_texte')
    ).all()

    domaine_choices = [(domaine.id_domaine, f"{domaine.theme_texte} - {domaine.domaine_texte}") for domaine in domaines]
    form.id_domaine.choices = domaine_choices

    if form.validate_on_submit():
        chapitre.texte = form.texte.data
        chapitre.id_domaine = form.id_domaine.data
        db.session.commit()
        flash('Chapitre updated successfully', 'success')
        return redirect(url_for('list_chapitres'))

    elif request.method == 'GET':
        form.id_domaine.data = chapitre.id_domaine
        form.texte.data = chapitre.texte

    return render_template('edit_chapitre.html', title='Edit Chapitre', form=form)

@edition.route('/edit/question/<int:id>', methods=['GET', 'POST'])
@log_action
@login_required
def edit_question(id):
    question = Question.query.get_or_404(id)
    form = QuestionForm()

    chapitres = Chapitre.query.join(Domaines, Domaines.id_domaine == Chapitre.id_domaine).join(Themes, Themes.id_theme == Domaine.id_theme).add_columns(
        Theme.id_theme.label('id_theme'),
        Theme.texte.label('theme_texte'),
        Domaine.id_domaine.label('id_domaine'),
        Domaine.texte.label('domaine_texte'),
        Chapitre.id_chapitre.label('id_chapitre'),
        Chapitre.texte.label('chapitre_texte')
    ).all()

    chapitre_choices = [(chapitre.id_chapitre, f"{chapitre.theme_texte} - {chapitre.domaine_texte} - {chapitre.chapitre_texte}") for chapitre in chapitres]
    form.id_chapitre.choices = chapitre_choices

    if form.validate_on_submit():
        question.texte = form.texte.data
        question.id_chapitre = form.id_chapitre.data
        db.session.commit()
        flash('Question updated successfully', 'success')
        return redirect(url_for('list_questions'))

    elif request.method == 'GET':
        form.id_chapitre.data = question.id_chapitre
        form.texte.data = question.texte

    return render_template('edit_question.html', title='Edit Question', form=form)

