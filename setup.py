# setup.py

from app.db import DB
from app.models import Base
from app.users import User

def setup_admin():
    db = DB()
    
    # Create admin user
    admin_user = User(
        first_name = "admin",
        last_name = "admin01#",
        email='admin@admin.com',
        password='admin01',  # You may want to hash the password before storing it
        user_type='admin'  # Specify the user type as admin
    )

    # Add admin user to the database
    db.add_user(admin_user.email, admin_user.password)
    print("Admin user created successfully.")

if __name__ == "__main__":
    setup_admin()
