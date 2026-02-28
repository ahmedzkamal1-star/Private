import traceback
from app import create_app
from database import db
from models import User

def run_test():
    app = create_app()
    with app.app_context():
        try:
            admin = User.query.filter_by(role='admin').first()
            if not admin:
                print("No admin user found.")
                return

            with app.test_request_context('/admin/posts'):
                from flask_login import login_user
                login_user(admin)
                response = app.full_dispatch_request()
                print("Status Code:", response.status_code)
                if response.status_code == 500:
                    print(response.get_data(as_text=True))
        except Exception as e:
            traceback.print_exc()

if __name__ == '__main__':
    run_test()
