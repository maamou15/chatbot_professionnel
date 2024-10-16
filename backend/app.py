from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  
from routes.api import api_blueprint
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "https://localhost:3000"}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.register_blueprint(api_blueprint)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    user_id = request.json.get("user_id", 'default_user')
    
    response_data = api_blueprint.handle_chat_message(user_input, user_id)
    
    response = jsonify(response_data)
    response.headers['Access-Control-Allow-Origin'] = 'https://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Custom-Header'] = 'YourCustomHeaderValue'

    return response

if __name__ == '__main__':
    app.run(ssl_context=('server.cert', 'server.key'), debug=True)
