# setup.py

from app.db import DB
from app.models import Base
from app.user.users import UserModel

def setup_admin():
    db = DB("sqlite:///database.db")
    
    # Create admin user
    admin_user = UserModel(
        first_name = "admin",
        last_name = "admin01#",
        email='admin@admin.com',
        password='admin01',  # You may want to hash the password before storing it
        role='admin'  # Specify the user type as admin
    )

    # Add admin user to the database
    db.add_user(admin_user.email, admin_user.password)
    print("Admin user created successfully.")

if __name__ == "__main__":
    setup_admin()
