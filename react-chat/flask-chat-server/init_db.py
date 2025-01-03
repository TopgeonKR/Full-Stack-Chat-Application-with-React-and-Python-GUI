from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()  # 모든 테이블 생성
    print("Database initialized successfully.")
