try:
    from app import create_app
    print("Attempting to create app...")
    app = create_app()
    print("App created successfully!")
    with app.app_context():
        from models import User
        print("Models imported!")
        u = User.query.first()
        print(f"Database connection successful! Found user: {u.full_name if u else 'No users'}")
except Exception as e:
    import traceback
    print("Error during startup:")
    traceback.print_exc()
