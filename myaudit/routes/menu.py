from myaudit import db, login_manager
from myaudit.utils import log_action
from myaudit.models import Missions, MissionDroits

from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user

menu = Blueprint('menu', __name__)

@menu.route('/dashboard', methods=['GET', 'POST'])
@log_action
@login_required
def dashboard():
    if current_user.is_admin():
        missions = Missions.query.join(MissionDroits).all()
    
    else:
        missions = Missions.query.join(MissionDroits).filter(MissionDroits.id_user == current_user.id_user, MissionDroits.droit.in_(['chef de projet', 'auditeur'])).all()
    
    return render_template('dashboard.html', title='Dashboard', missions=missions, user=current_user)