# Exemple simple 
# Auteur: CHATGPT
# Relecture : non
# Objectif : oui 

def get_data():
    return [
        {"model": "Themes", "data":{"id_theme":11, "theme": "Exemple"}},
        {"model": "Domaines", "data":{"id_theme":11, "id_domaine":111, "domaine": "Audit simple"}},
        {"model": "Chapitres", "data":{"id_domaine":111, "id_chapitre":1111, "chapitre": "Réseaux"}},
        {"model": "Questions", "data":{"id_chapitre":1111, "question": "Quels types de pare-feu sont utilisés sur votre réseau ?", "objectif": "La vérification de l'existence et de l'efficacité des mécanismes de protection réseau est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1111, "question": "Utilisez-vous un système de détection et de prévention d'intrusion (IDS/IPS) ?", "objectif": "La mise en place de systèmes de surveillance des activités malveillantes est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1111, "question": "Les accès à distance (VPN, RDP) sont-ils sécurisés et journalisés ?", "objectif": "La sécurisation et la journalisation des connexions à distance sont jugées ..."}},
        {"model": "Questions", "data":{"id_chapitre":1111, "question": "Existe-t-il des segments réseau pour séparer les environnements sensibles ?", "objectif": "La segmentation réseau est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1111, "question": "Les systèmes critiques sont-ils surveillés en continu (SIEM, surveillance réseau) ?", "objectif": "La surveillance continue des systèmes critiques est jugée ..."}},
        {"model": "Chapitres", "data":{"id_domaine":111, "id_chapitre":1112, "chapitre": "Systèmes"}},
        {"model": "Questions", "data":{"id_chapitre":1112, "question": "Les systèmes sont-ils mis à jour régulièrement avec les derniers correctifs ?", "objectif": "La régularité des mises à jour est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1112, "question": "Les systèmes d'exploitation sont-ils tous pris en charge et non obsolètes ?", "objectif": "La vérification de l'utilisation de systèmes pris en charge est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1112, "question": "Les mises à jour logicielles sont-elles testées avant leur déploiement en production ?", "objectif": "Le test des mises à jour est jugé ..."}},
        {"model": "Questions", "data":{"id_chapitre":1112, "question": "Les fichiers de configuration sensibles (serveurs, bases de données) sont-ils correctement protégés ?", "objectif": "La protection des fichiers de configuration est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1112, "question": "Les dispositifs USB et autres médias amovibles sont-ils contrôlés ?", "objectif": "Le contrôle des médias amovibles est jugé ..."}},
        {"model": "Chapitres", "data":{"id_domaine":111, "id_chapitre":1113, "chapitre": "Journalisation et monitoring"}},
        {"model": "Questions", "data":{"id_chapitre":1113, "question": "Les accès aux serveurs critiques sont-ils journalisés et surveillés en temps réel ?", "objectif": "La journalisation et la surveillance des accès sont jugées ..."}},
        {"model": "Questions", "data":{"id_chapitre":1113, "question": "Les logs sont-ils centralisés et conservés suffisamment longtemps pour permettre une analyse post-incident ?", "objectif": "La centralisation et la conservation des logs sont jugées ..."}},
        {"model": "Questions", "data":{"id_chapitre":1113, "question": "Les accès à distance (VPN, RDP) sont-ils sécurisés et journalisés ?", "objectif": "La sécurisation et la journalisation des connexions à distance sont jugées ..."}},
        {"model": "Questions", "data":{"id_chapitre":1113, "question": "Effectuez-vous des tests d’intrusion (pentests) de manière régulière ?", "objectif": "La réalisation de tests d'intrusion est jugée ..."}},
        {"model": "Chapitres", "data":{"id_domaine":111, "id_chapitre":1114, "chapitre": "Gestion des accès"}},
        {"model": "Questions", "data":{"id_chapitre":1114, "question": "Avez-vous une politique de gestion des accès basée sur le principe du moindre privilège ?", "objectif": "La mise en place de ce principe est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1114, "question": "Les droits des utilisateurs sont-ils révisés régulièrement pour éviter des privilèges excessifs ?", "objectif": "La révision régulière des droits est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1114, "question": "Les comptes administratifs sont-ils séparés des comptes utilisateurs standards ?", "objectif": "La séparation des comptes est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1114, "question": "Utilisez-vous une authentification multi-facteurs (MFA) pour les accès sensibles ?", "objectif": "L'utilisation de l'authentification multi-facteurs est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1114, "question": "Les comptes inactifs sont-ils désactivés ou supprimés ?", "objectif": "La désactivation ou suppression des comptes inactifs est jugée ..."}},
        {"model": "Chapitres", "data":{"id_domaine":111, "id_chapitre":1115, "chapitre": "Sécurité des données"}},
        {"model": "Questions", "data":{"id_chapitre":1115, "question": "Utilisez-vous le chiffrement pour protéger les données sensibles en transit et au repos ?", "objectif": "L'utilisation du chiffrement est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1115, "question": "Avez-vous une politique de classification et de gestion des données sensibles ?", "objectif": "La mise en place de cette politique est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1115, "question": "Les clés de chiffrement sont-elles stockées de manière sécurisée ?", "objectif": "Le stockage sécurisé des clés de chiffrement est jugé ..."}},
        {"model": "Questions", "data":{"id_chapitre":1115, "question": "Utilisez-vous une solution de gestion des identités et des accès (IAM) en place ?", "objectif": "L'implémentation d'une solution IAM est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1115, "question": "Les mots de passe sont-ils stockés sous forme chiffrée et avec un sel ?", "objectif": "Le chiffrement des mots de passe avec un sel est jugé ..."}},
        {"model": "Chapitres", "data":{"id_domaine":111, "id_chapitre":1116, "chapitre": "Politiques de sécurité"}},
        {"model": "Questions", "data":{"id_chapitre":1116, "question": "Avez-vous une politique de gestion des mots de passe (longueur, complexité) ?", "objectif": "L'existence d'une telle politique est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1116, "question": "Des audits de sécurité internes ou externes sont-ils réalisés régulièrement ?", "objectif": "La réalisation régulière d'audits est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1116, "question": "Avez-vous une procédure de réponse aux incidents de sécurité ?", "objectif": "L'existence d'une procédure de réponse aux incidents est jugée ..."}},
        {"model": "Questions", "data":{"id_chapitre":1116, "question": "Avez-vous une politique de contrôle des accès physiques aux serveurs ?", "objectif": "Le contrôle des accès physiques est jugé ..."}},
        {"model": "Questions", "data":{"id_chapitre":1116, "question": "Avez-vous un plan de continuité d'activité en cas d'incident majeur ?", "objectif": "L'élaboration d'un plan de continuité d'activité est jugée ..."}},
        {"model": "Chapitres", "data":{"id_domaine":111, "id_chapitre":1117, "chapitre": "Sauvegarde et récupération"}},
        {"model": "Questions", "data":{"id_chapitre":1117, "question": "Existe-t-il une solution de sauvegarde des données, et est-elle régulièrement testée ?", "objectif": "La mise en place et le test régulier d'une solution de sauvegarde sont jugés ..."}}
    ]


