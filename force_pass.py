from app import create_app
from database import db
from models import User

app = create_app()
with app.app_context():
    user = User.query.filter_by(code='2023001').first()
    if user:
        user.set_password('123456')
        db.session.commit()
        print("Password updated for 2023001")
    else:
        print("User not found")
