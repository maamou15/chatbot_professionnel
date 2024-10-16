from flask import Blueprint, jsonify, request
from models.utilisateurs import Utilisateur
from models.database import db
import requests
from flask_cors import CORS

api_blueprint = Blueprint('api', __name__)
CORS(api_blueprint, resources={r"/chat": {"origins": "https://localhost:3000"}})


ADZUNA_API_ID = 'afd31b98'
ADZUNA_API_KEY = '36817b8a29594593b68f141e83c49d0b'
ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/fr/search/1"

user_conversations = {}

def handle_chat_message(user_input, user_id):
    conversation = user_conversations.get(user_id, {'state': 'initial'})
    response = ""

    if conversation['state'] == 'initial':
        response = "Bienvenue! Souhaitez-vous vous inscrire ou vous connecter?"
        conversation['state'] = 'awaiting_action'
    elif conversation['state'] == 'awaiting_action':
        if "inscrire" in user_input.lower():
            conversation['state'] = 'awaiting_registration_info'
            response = "Entrez votre nom, prénom, téléphone, email et mot de passe (séparés par des virgules)."
        elif "connecter" in user_input.lower():
            conversation['state'] = 'awaiting_login_info'
            response = "Entrez votre email et mot de passe (séparés par une virgule)."
        else:
            response = "Je n'ai pas compris. Souhaitez-vous vous inscrire ou vous connecter?"
    elif conversation['state'] == 'awaiting_registration_info':
        user_data = user_input.split(',')
        if len(user_data) == 5:
            nom, prenom, telephone, email, password = [x.strip() for x in user_data]
            new_user = Utilisateur(nom=nom, prenom=prenom, telephone=telephone, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            response = "Inscription réussie. Vous pouvez maintenant vous connecter."
            conversation['state'] = 'initial'
        else:
            response = "Informations incorrectes. Veuillez entrer: nom, prénom, téléphone, email et mot de passe."
    elif conversation['state'] == 'awaiting_login_info':
        login_data = user_input.split(',')
        if len(login_data) == 2:
            email, password = [x.strip() for x in login_data]
            user = Utilisateur.query.filter_by(email=email).first()
            if user and user.check_password(password):
                response = "Connexion réussie. Que souhaitez-vous faire? Rechercher un emploi?"
                conversation['state'] = 'awaiting_job_search'
            else:
                response = "Identifiants incorrects. Réessayez."
        else:
            response = "Veuillez entrer l'email et le mot de passe séparés par une virgule."
    elif conversation['state'] == 'awaiting_job_search':
        response = "Quel type d'emploi recherchez-vous?"
        conversation['state'] = 'awaiting_job_query'
    elif conversation['state'] == 'awaiting_job_query':
        query = user_input.strip()
        url = f"{ADZUNA_BASE_URL}?app_id={ADZUNA_API_ID}&app_key={ADZUNA_API_KEY}&what={query}"
        adzuna_response = requests.get(url)
        if adzuna_response.status_code == 200:
            job_data = adzuna_response.json().get('results', [])
            if job_data:
                job_offers = [
                    f"{job.get('title')} chez {job.get('company', {}).get('display_name', 'N/A')} à {job.get('location', {}).get('display_name', 'N/A')}"
                    for job in job_data
                ]
                response = "\n".join(job_offers) if job_offers else "Aucune offre trouvée."
            else:
                response = "Aucune offre trouvée."
        else:
            response = f"Erreur lors de la récupération des offres: {adzuna_response.status_code}"
        conversation['state'] = 'initial'

    user_conversations[user_id] = conversation
    return jsonify({"response": response})

@api_blueprint.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'OK'}), 200  # Répondre avec un statut 200 pour OPTIONS
    data = request.get_json()
    user_input = data.get('message')
    user_id = data.get('user_id', 'default_user')
    return handle_chat_message(user_input, user_id)

