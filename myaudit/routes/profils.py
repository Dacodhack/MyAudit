from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from myaudit import db
from myaudit.models import Users, Logs
from myaudit.utils import log_action

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

profils = Blueprint('profils', __name__)
ph = PasswordHasher()

@profils.route('/profil', methods=['GET', 'POST'])
@log_action
@login_required
def profil():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        new_password = request.form.get('password')
        if new_password:
            hashed_password = ph.hash(new_password)
            current_user.password = hashed_password 
        try:
            db.session.commit()
        except:
            return render_template('erreur.html', erreur="Problème de changement d'utilisateur ou mot de passe")
        flash('Votre profil a été mis à jour.', 'success')
        return redirect(url_for('profils.profil'))

    return render_template('profil.html', title='Mon Profil', user=current_user)


@profils.route('/admin/users', methods=['GET', 'POST'])
@log_action
@login_required
def manage_users():
    if not current_user.is_admin():
        flash('Accès refusé.', 'danger')
        return redirect(url_for('profils.profil'))

    users = Users.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        action = request.form.get('action')  
        user = Users.query.get(user_id)
        
        if user:
            if action == 'promote':
                if user.droits_generaux != 'admin':  
                    user.droits_generaux = 'admin'
                    db.session.commit()
                    flash(f"L'utilisateur {user.username} a été promu administrateur.", 'success')
                else:
                    flash(f"L'utilisateur {user.username} est déjà administrateur.", 'warning')
            elif action == 'demote':
                if user.droits_generaux == 'admin':  
                    user.droits_generaux = None  
                    db.session.commit()
                    flash(f"L'utilisateur {user.username} a été rétrogradé.", 'success')
                else:
                    flash(f"L'utilisateur {user.username} n'est pas administrateur.", 'warning')
            elif action == 'delete':
                db.session.delete(user)
                db.session.commit()
                flash(f"L'utilisateur {user.username} a été supprimé.", 'success')
        else:
            flash("Utilisateur non trouvé.", 'danger')

        return redirect(url_for('profils.manage_users'))

    return render_template('manage_users.html', title='Gestion des utilisateurs', users=users)


@profils.route('/logs', methods=['GET', 'POST'])
@log_action
@login_required
def logs():
    logs = Logs.query.all()
    return render_template('logs.html', title='Mon Profil', logs=logs)