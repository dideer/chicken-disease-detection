from pathlib import Path

from flask import Flask, redirect, send_from_directory
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import psycopg2

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, SECRET_KEY

bcrypt = Bcrypt()


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def create_app():
    project_frontend_dir = Path(__file__).resolve().parents[2] / 'frontend'
    upload_dir = Path(__file__).resolve().parents[1] / 'frontend' / 'uploads'

    app = Flask(
        __name__,
        static_folder=str(project_frontend_dir),
        static_url_path=''
    )
    app.config['SECRET_KEY'] = SECRET_KEY

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    bcrypt.init_app(app)

    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.predict import predict_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return redirect('/dashboard.html')

    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(upload_dir, filename)

    @app.route('/<path:path>')
    def serve_frontend(path):
        return send_from_directory(app.static_folder, path)

    return app
