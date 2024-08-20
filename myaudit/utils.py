from functools import wraps

from flask import request, redirect, url_for, flash, render_template
from flask_login import current_user

from myaudit import db
from myaudit.models import MissionDroits, Logs

from datetime import datetime
import re

def log_action(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = current_user.username if current_user.is_authenticated else 'Anonymous'
        if request.method == 'POST':
            post_data = request.get_data(as_text=True)
            masked_data = mask_password(post_data)  
            log_entry = Logs(user=user, url=request.url, sended=masked_data)
        else:    
            log_entry = Logs(user=user, url=request.url, sended='ELSE')
        db.session.add(log_entry)
        db.session.commit()
        return func(*args, **kwargs)
    return decorated_function

def check_permissions(get_id_mission, required_roles=['chef de projet', 'auditeur']):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            id_mission = get_id_mission(*args, **kwargs)
            is_allow = db.session.query(MissionDroits).filter(
                MissionDroits.id_mission == id_mission,
                MissionDroits.id_user == current_user.id_user,
                MissionDroits.droit.in_(required_roles)
            ).first() is not None
            if not is_allow and not current_user.is_admin():
                flash('Access denied', 'danger')
                return render_template('erreur.html', erreur="check_permissions - Page refusée")
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def mask_password(data):
    masked_data = re.sub(r'(password=)[^&]*', r'\1********', data)
    return masked_data