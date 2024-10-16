# routes/jobs.py
from flask import Blueprint, request, jsonify

jobs = Blueprint('jobs', __name__)

@jobs.route('/search', methods=['GET'])
def search_jobs():
    region = request.args.get('region')
    sector = request.args.get('sector')
    
    # Filtrer les jobs en fonction de la région et du secteur
    job_list = [
        {"title": "Développeur Python", "region": "Paris", "sector": "IT"},
        {"title": "Analyste de Données", "region": "Lyon", "sector": "Data"}
    ]
    filtered_jobs = [job for job in job_list if (not region or job["region"] == region) and (not sector or job["sector"] == sector)]
    return jsonify(filtered_jobs)