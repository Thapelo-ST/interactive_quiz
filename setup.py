# setup.py

from app.db import DB
from app.user.users import UserModel
from werkzeug.security import generate_password_hash

def setup_admin():
    try:
        # Initialize database connection
        db = DB("sqlite:///database.db")
        
        # Check if admin user already exists
        if db.get_user_by_email('admin@admin.com'):
            print("Admin user already exists.")
            return

        # Create admin user instance
        admin_user = UserModel(
            first_name="Admin",
            last_name="User",
            email='admin@admin.com',
            password=generate_password_hash('admin01'),  # Hash the password before storing it
            role='admin'  # Specify the user type as admin
        )

        # Add admin user to the database
        db.add_user(admin_user)
        print("Admin user created successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    setup_admin()
