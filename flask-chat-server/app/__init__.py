from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS  # CORS 추가
import os

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    
    # 절대 경로를 사용하여 데이터베이스 경로 설정
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, '../instance/passwords.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    CORS(app, supports_credentials=True)

    # 데이터베이스 테이블 생성
    with app.app_context():
        db.create_all()

    # 라우트 등록
    from .routes import main
    app.register_blueprint(main)

    return app 
