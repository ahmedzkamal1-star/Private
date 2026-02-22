from app import create_app, db
from models import User

app = create_app()
with app.app_context():
    # Attempt to find the admin by code 'admin' or by checking the admin role
    admin = User.query.filter_by(code='admin').first()
    if not admin:
        admin = User.query.filter_by(role='admin').first()
        
    if admin:
        print(f"Admin found: {admin.full_name} (Code: {admin.code})")
        admin.set_password('Riko00ooAa#')
        db.session.commit()
        print("Admin password updated to 'Riko00ooAa#' successfully.")
    else:
        print("Admin user not found in the database.")
