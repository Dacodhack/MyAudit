# Description du Site Web d'Audit de Sécurité
## Description Générale du Site Web
Le site web que nous avons construit est une plateforme d'audit de sécurité, permettant aux utilisateurs d'exécuter, de gérer et de générer des rapports d'audit pour des missions spécifiques. Ce site est conçu pour les auditeurs de sécurité et les chefs de projet, leur fournissant des outils pour suivre et documenter les audits de sécurité.
## Fonctionnalités Clés
### 1. Authentification et Autorisation
 - Inscription et Connexion :
     - Les utilisateurs peuvent s'inscrire et se connecter de manière sécurisée.
     - Les mots de passe sont stockés de manière sécurisée avec un hashage approprié.
 - Gestion des Droits d'Accès :
     - Les utilisateurs sont assignés à des missions avec des rôles spécifiques tels que "auditeur" ou "chef de projet".
     - Les utilisateurs ne peuvent accéder qu'aux missions pour lesquelles ils ont été explicitement autorisés.
### 2. Gestion des Missions d'Audit
 - Création et Édition de Missions :
     - Les utilisateurs peuvent créer de nouvelles missions d'audit, spécifiant des détails tels que le nom de la mission, le nom du client, le produit audité, les représentants, etc.
     - Les missions peuvent être modifiées pour mettre à jour les informations au fur et à mesure de l'avancement de l'audit.
 - Affichage des Missions :
     - Les utilisateurs peuvent voir une liste des missions auxquelles ils ont accès, avec des détails sur chaque mission.
### 3. Questionnaire d'Audit
 - Formulaire de Réponses :
     - Les auditeurs peuvent répondre à des questions spécifiques pour chaque mission à l'aide d'un formulaire.
     - Le formulaire inclut un champ de texte pour des réponses détaillées, un champ de téléchargement de fichiers pour les pièces jointes, et une liste déroulante pour évaluer les mesures de sécurité (avec des options de 0 à 5, où chaque valeur représente un niveau de mise en œuvre des mesures).
 - Validation et Soumission :
     - Les réponses aux questions sont validées avant soumission pour s'assurer de la complétude et de la pertinence des informations fournies.
### 4. Génération de Rapports
 - Rapports en LaTeX :
     - Les utilisateurs peuvent générer des rapports d'audit en format LaTeX. Le modèle LaTeX est personnalisé pour inclure les détails spécifiques de chaque mission d'audit.
     - Les rapports peuvent inclure des images encodées en base64 et sont compilés en différents formats, tels que PDF et DOCX, à l'aide de Pandoc.
 - Téléchargement de Rapports :
     - Une fois générés, les rapports peuvent être téléchargés directement depuis le site web.
### 5. Gestion des Fichiers
 - Téléchargement de Pièces Jointes :
     - Les auditeurs peuvent télécharger des fichiers pertinents pour chaque mission, tels que des preuves de vulnérabilités, des captures d'écran, etc.
     - Les fichiers sont sauvegardés de manière organisée dans un répertoire dédié.
## Objectifs du Site Web
 - Centralisation de l'Information :
Fournir une plateforme unique où les auditeurs peuvent gérer toutes les informations relatives à leurs missions d'audit de sécurité.
 - Facilitation de la Collaboration :
Permettre aux équipes d'audit de travailler ensemble de manière efficace en offrant des outils pour le partage d'informations et la coordination des tâches.
 - Automatisation des Rapports :
Simplifier le processus de génération de rapports d'audit, réduisant ainsi le temps et les efforts nécessaires pour produire des documents de haute qualité.
 - Sécurisation des Données :
Assurer la sécurité des informations sensibles en contrôlant les accès et en utilisant des pratiques de gestion sécurisée des mots de passe et des fichiers.
## Conclusion
Le site web d'audit de sécurité que nous avons développé est une solution complète pour la gestion et la documentation des audits de sécurité. Avec des fonctionnalités robustes d'authentification, de gestion des missions, de génération de rapports et de gestion des fichiers, il permet aux auditeurs de travailler de manière plus organisée, efficace et sécurisée.
