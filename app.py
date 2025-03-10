import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Load the secret key from an environment variable (stored as hex) and convert it back to bytes.
secret_key_hex = os.environ.get('SECRET_KEY')
if secret_key_hex:
    app.config['SECRET_KEY'] = bytes.fromhex(secret_key_hex)
else:
    # Fallback key for local development (not recommended for production)
    app.config['SECRET_KEY'] = b'\xfa\t\xb8\xab`\x1b\xcd\x88\xea\xf2\xbb!(\x17\xb4ZA\xe7~\xa8\xa3}\xc1\x0c'

# Configure SQLite database (the file 'users.db' is created automatically)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Register blueprints
from auth import auth_bp
from analysis import analysis_bp

app.register_blueprint(auth_bp)
app.register_blueprint(analysis_bp)

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
