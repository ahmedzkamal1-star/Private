import os
from flask import Flask
from dotenv import load_dotenv
from config import Config
from database import db

load_dotenv() # لقراءة متغيرات البيئة من ملف .env

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # CORS support for mobile app
    @app.after_request
    def after_request(response):
        origin = response.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Auth-Token'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return response

    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Allow API login without redirect
    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import request, jsonify, redirect, url_for
        if request.path.startswith('/api/') or request.headers.get('X-Auth-Token'):
            return jsonify({"error": "Authentication required"}), 401
        return redirect(url_for('main.login'))

    with app.app_context():
        # Import parts of our application
        from models import User, Course, Enrollment 
        db.create_all()

    from routes import main
    app.register_blueprint(main)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
