# setup.py

from app.db import DB
from app.users import User

def setup_admin():
    db = DB()
    
    # Check if admin user already exists
    admin_email = 'admin@admin.com'
    existing_admin = db.find_user_by(email=admin_email)
    if existing_admin:
        print("Admin user already exists.")
        return

    # Create admin user
    admin_user = User(
        email='admin@admin.com',
        password='admin01',  # You may want to hash the password before storing it
        user_type='admin'  # Specify the user type as admin
    )

    # Add admin user to the database
    db.add_user(admin_user.email, admin_user.password, admin_user.user_type)
    print("Admin user created successfully.")

if __name__ == "__main__":
    setup_admin()
