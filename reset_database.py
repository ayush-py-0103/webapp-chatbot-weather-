import os
from app import app, db  # yahan se Flask app aur SQLAlchemy db import karo

# Database file path
db_path = "instance/chat_history.db"  # correct path

# Agar file exist kare to delete karo
if os.path.exists(db_path):
    os.remove(db_path)
    print("Existing database deleted.")

# Flask app context me dobara create karo
with app.app_context():
    db.create_all()
    print("New empty database created.")