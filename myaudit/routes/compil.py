import markdown2, re

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_user, logout_user, current_user, login_required, logout_user

from jinja2 import Template

from sqlalchemy import or_

from werkzeug.utils import secure_filename
from io import BytesIO

from myaudit import db, login_manager

from myaudit.models import Missions, MissionDroits, Domaines, Themes, Chapitres, Questions, QuestionsCache, MissionReponse, RecommendationsAudit
from myaudit.forms import MissionForm, QuestionnaireForm
from myaudit.utils import log_action, check_permissions

from sqlalchemy import or_

import datetime, os, tempfile, subprocess, yaml

compil = Blueprint('compil', __name__)
current_dir = os.path.dirname(os.path.abspath(__file__))


#region Convention
@compil.route('/gen_convention/<int:id_mission>', methods=['GET'])
@log_action
@login_required
@check_permissions(lambda id_mission: id_mission, required_roles=['chef de projet', 'auditeur'])
def gen_convention(id_mission):
    with open(current_dir+'/../templates/latex/template_convention.tex') as file:
        template_content = file.read()
    variables = get_mission_data_as_yaml(id_mission)
    template = Template(template_content)
    output_content = template.render(variables)

    tmp_convention_tex = tempfile.NamedTemporaryFile(delete=False, suffix='.tex')
    tmp_convention_docx = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    
    fichier = open(tmp_convention_tex.name, "w")
    fichier.write(output_content)
    fichier.close()
    
    try:
        subprocess.run(['pandoc', tmp_convention_tex.name, '-o', tmp_convention_docx.name], check=True)
    except:
        return render_template('erreur.html', erreur="Erreur de compilation avec Pandoc")
    
    try:
        with open(tmp_convention_docx.name, 'rb') as output_file:
            buffer = BytesIO(output_file.read())
        buffer.seek(0)
        flash('Report generated successfully', 'success')
        return send_file(buffer, as_attachment=True, download_name=f'convention_{id_mission}_{datetime.datetime.today()}.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except:
        return render_template('erreur.html', erreur="Erreur lors de la génération du rapport")
    finally:
        if os.path.exists(tmp_convention_tex.name):
            os.remove(tmp_convention_tex.name)
        if os.path.exists(tmp_convention_docx.name):
            os.remove(tmp_convention_docx.name)


#region Contrat
@compil.route('/gen_contrat/<int:id_mission>', methods=['GET'])
@log_action
@login_required
@check_permissions(lambda id_mission: id_mission, required_roles=['chef de projet', 'auditeur'])
def gen_contrat(id_mission):
    with open(current_dir+'/../templates/latex/template_contrat.tex') as file:
        template_content = file.read()
    variables = get_mission_data_as_yaml(id_mission)
    template = Template(template_content)
    output_content = template.render(variables)

    tmp_contrat_tex = tempfile.NamedTemporaryFile(delete=False, suffix='.tex')
    tmp_contrat_docx = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
    
    fichier = open(tmp_contrat_tex.name, "w")
    fichier.write(output_content)
    fichier.close()
    
    try:
        subprocess.run(['pandoc', tmp_contrat_tex.name, '-o', tmp_contrat_docx.name], check=True)
    except:
        return render_template('erreur.html', erreur="Erreur de compilation avec Pandoc")
    
    try:
        with open(tmp_contrat_docx.name, 'rb') as output_file:
            buffer = BytesIO(output_file.read())
        buffer.seek(0)
        flash('Report generated successfully', 'success')
        return send_file(buffer, as_attachment=True, download_name=f'contrat_{id_mission}_{datetime.datetime.today()}.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except:
        return render_template('erreur.html', erreur="Erreur lors de la génération du rapport")
    finally:
        if os.path.exists(tmp_contrat_tex.name):
            os.remove(tmp_contrat_tex.name)
        if os.path.exists(tmp_contrat_docx.name):
            os.remove(tmp_contrat_docx.name)

#region Rapport
@compil.route('/gen_rapport/<int:id_mission>', methods=['GET']) # redondant peut être éditer ça
@log_action
@login_required
@check_permissions(lambda id_mission: id_mission, required_roles=['chef de projet', 'auditeur'])
def gen_rapport(id_mission):
    with open(current_dir+'/../templates/latex/template_rapport.tex') as file:
        template_content = file.read()
    variables = get_mission_data_as_yaml(id_mission)
    template = Template(template_content)
    output_content = template.render(variables)

    tmp_rapport_tex = tempfile.NamedTemporaryFile(delete=False, suffix='.tex')
    tmp_rapport_docx = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')

    content_rapport = gen_content_rapport(id_mission)
    fichier = open(tmp_rapport_tex.name, "w")
    fichier.write(output_content)
    fichier.write(content_rapport)
    fichier.close()

    try:
        subprocess.run(['pandoc', tmp_rapport_tex.name, '-o', tmp_rapport_docx.name], check=True)
    except:
        return render_template('erreur.html', erreur="Erreur de compilation avec Pandoc")

    try:
        with open(tmp_rapport_docx.name, 'rb') as output_file:
            buffer = BytesIO(output_file.read())
        buffer.seek(0)
        flash('Report generated successfully', 'success')
        return send_file(buffer, as_attachment=True, download_name=f'rapport_{id_mission}_{datetime.datetime.today()}.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except:
        return render_template('erreur.html', erreur="Erreur lors de la génération du rapport")
    finally:
        if os.path.exists(tmp_rapport_tex.name):
            os.remove(tmp_rapport_tex.name)
        if os.path.exists(tmp_rapport_docx.name):
            os.remove(tmp_rapport_docx.name)


#region FONCTIONS ANNEXES

def get_mission_data_as_yaml(id_mission):
    mission = db.session.query(Missions).filter_by(id_mission=id_mission).first()
    if not mission:
        return None
    mission_data = {
        'mission': mission.mission,
        'clientname': mission.client_name,
        'clientcompany': mission.client_company,
        'clientaddress': mission.client_address,
        'clientsiren': mission.client_siren,
        'clientproduit': mission.client_produit,
        'clientrepresentative': mission.client_representative,
        'clienttitle': mission.client_title,
        'auditorname': "David Perez",
        'auditorcompany': "byDacodhack",
        'auditoraddress': "42 rue de l'aiguillerie, 34000 Montpellier",
        'auditorsiren': "922793989",
        'auditorrepresentative': "David Perez",
        'auditortitle': "Auditeur",
        'AUDITORLOGO': './../MyAudit/myaudit/templates/logo/logo.png', # Attention au chemin pour avoir le logo
        'VERSIONDOCUMENT': "v-1.0",
        'DATEDOCUMENT': datetime.datetime.today()
        }
    return mission_data
    

def gen_content_rapport(id_mission):
    reponses_list = MissionReponse.query.filter_by(id_mission=id_mission).join(Missions, Missions.id_mission == MissionReponse.id_mission).join(Domaines, Domaines.id_domaine == Missions.id_domaine).join(Chapitres, Chapitres.id_domaine == Domaines.id_domaine).order_by(Chapitres.id_chapitre.desc()).all()
    reponses = [ra.to_dict() for ra in reponses_list]

    latex_content = []
    dernier_chapitre = None
    mega_tableau = []
    chemin_images = current_dir + "../upload/"

    for reponse in reponses:   
        # Rédaction des chapitres
        chapitre = reponse["chapitre"]
        if chapitre != dernier_chapitre:
            latex_content.append(r"\chapter{" + chapitre + r"}")
            dernier_chapitre = chapitre
            e_s_es = re.search(r'jugé(?:e)?(?:s)?(.*)', reponse["objectif"]).group(0).strip().split(" ")[0].replace("jugé","")
        # Rédaction des objectifs si existant 

        if reponse["objectif"]:
            if reponse["evaluation"] == 0: 
                objectif_atteint = reponse["objectif"].replace('...', ("non évaluable"+e_s_es).replace('ee', 'e'))
            if reponse["evaluation"] == 1: 
                objectif_atteint = reponse["objectif"].replace('...', "inexistant"+e_s_es)
            if reponse["evaluation"] == 2: 
                objectif_atteint = reponse["objectif"].replace('...', "en cours de réflexion")
            if reponse["evaluation"] == 3: 
                objectif_atteint = reponse["objectif"].replace('...', "en cours d’implémentation")
            if reponse["evaluation"] == 4: 
                objectif_atteint = reponse["objectif"].replace('...', "implémenté"+e_s_es)
            if reponse["evaluation"] == 5: 
                objectif_atteint = reponse["objectif"].replace('...', "implémenté"+e_s_es+" avec procédures associées")
            latex_content.append(r"\subsubsection{" + objectif_atteint + "}")
        else:
            latex_content.append(r"\textit{" + reponse["question"] + r"}:")
            if reponse["evaluation"] == 0: 
                objectif_atteint = (r"\textit{Mesures non évaluable}")
            if reponse["evaluation"] == 1: 
                objectif_atteint = (r"\textit{Mesures inexistantes}")
            if reponse["evaluation"] == 2: 
                objectif_atteint = (r"\textit{Mesures en cours de réflexion}")
            if reponse["evaluation"] == 3: 
                objectif_atteint = (r"\textit{Mesures en cours d’implémentation}")
            if reponse["evaluation"] == 4: 
                objectif_atteint = (r"\textit{Mesures implémentées}")
            if reponse["evaluation"] == 5: 
                objectif_atteint = (r"\textit{Mesures implémentées avec procédures associées}")
            latex_content.append(r"\textbf{" + objectif_atteint + "}")
      
        if reponse["réponse"]:
            latex_content.append(r"\paragraph{}" + reponse["réponse"])
        if reponse["piece_jointe"] and os.path.exists(os.path.join(chemin_images, reponse["piece_jointe"])):
            latex_content.append(r"\includegraphics[width=\textwidth]{" + os.path.join(chemin_images, reponse["piece_jointe"]) + r"}")

        questioncache = QuestionsCache.query.filter_by(id_mission=id_mission, id_question=reponse["id_question"]).first()
        recommendations_audit_list = RecommendationsAudit.query.filter_by(id_questionsCache=questioncache.id_questionsCache).all()
        recommandations = [ra.to_dict() for ra in recommendations_audit_list]
        
        if recommandations: # Cette fois pour les reco

            latex_content.append(r"\paragraph{Recommendations:}")

            for reco in recommandations:
                latex_content.append("\\begin{tabular}{|c|c|}\n")
                latex_content.append("\\hline\n")
                latex_content.append("Titre de la Recommandation & Priorité \\\\\n")
                latex_content.append("\\hline\n")

                reco_titre = reco.get("titre_reco", "N/A")
                reco_recommendation = reco.get("recommendation", "N/A")
                reco_sources = reco.get("sources", "N/A")        
                reco_r_prio = reco.get("r_prio", "N/A")

                latex_content.append(reco_titre + " & " + str(reco_r_prio) + " \\\\\n")
                latex_content.append("\\hline\n")
                latex_content.append("\\multicolumn{2}{|l|}{" + reco_recommendation + "}\\\\\n")
                latex_content.append("\\hline\n")
                latex_content.append("\\multicolumn{2}{|l|}{Sources: " + (reco_sources or "N/A") + "}\\\\\n")
                latex_content.append("\\hline\n")
                latex_content.append("\\end{tabular}\n")
        
        if recommandations: # Cette fois ce sont les vulnérabilités
            latex_content.append(r"\paragraph{Vulnérabilités:}")
            for vuln in recommandations:
                if vuln.get("vuln", "N/A"):
                    latex_content.append("\\begin{tabular}{|c|c|}\n")
                    latex_content.append("\\hline\n")
                    latex_content.append("Titre de la Vulnérabilité & Détails \\\\\n")
                    latex_content.append("\\hline\n")

                    vuln_titre_vuln = vuln.get("titre_vuln", "N/A")
                    vuln_vuln = vuln.get("vuln", "N/A")
                    vuln_v_impact = vuln.get("v_impact", "N/A")                
                    vuln_v_proba = vuln.get("v_proba", "N/A") 

                    latex_content.append(vuln_titre_vuln + " & " + vuln_vuln + " \\\\\n")
                    latex_content.append("\\hline\n")
                    latex_content.append("\\multicolumn{2}{|l|}{Impact: " + str(vuln_v_impact) + ", Probabilité: " + str(vuln_v_proba) + "}\\\\\n")
                    latex_content.append("\\hline\n")
                    latex_content.append("\\end{tabular}\n")

    latex_content.append(r"\newpage")
    latex_content.append(r"\section{Résumé des recommandations et vulnérabilités}")

    # Ajouter un tableau récapitulatif des titres de recommandations et vulnérabilités
    latex_content.append(r"\begin{tabular}{|l|l|}")
    latex_content.append(r"\hline")
    latex_content.append(r"Titre de la recommandation & Titre de la vulnérabilité \\")
    latex_content.append(r"\hline")
    for reco in recommandations:
        print(reco)
        reco_titre = reco.get("titre_reco", "N/A")
        vuln_titre_vuln = vuln.get("titre_vuln", "N/A")
        latex_content.append(f"{reco_titre} & {vuln_titre_vuln} \\\\")
        latex_content.append(r"\hline")
    latex_content.append(r"\end{tabular}")

    latex_content.append(r"\end{document}")

    # Convertir la liste en string pour sauvegarder dans un fichier
    rapport_latex = "\n".join(latex_content)
    return rapport_latex


    