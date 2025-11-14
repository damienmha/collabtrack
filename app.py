# app.py

from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from database import db
import os 
from flask_bcrypt import Bcrypt
from models import User, Project, Version
from s3_upload import upload_file_to_s3, allowed_file
from werkzeug.utils import secure_filename

# INITIALIZE APP & CONFIG

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration from the Config class in config.py
    # This automatically loads all your DB and AWS settings from .env
    app.config.from_object(Config)

    # CRITICAL FIX: Explicitly set Flask's secret_key
    app.secret_key = app.config['SECRET_KEY']

    # INITIALIZE EXTENSIONS 
    
    # Initialize SQLAlchemy with the application instance
    db.init_app(app) 
    
    # Initialize Bcrypt for password hashing
    global bcrypt
    bcrypt = Bcrypt(app)
    
    # BASIC ROUTE TEST
    
    @app.route('/')
    def home():
        """A simple test route to ensure the app is running."""
        # This confirms config is loaded correctly
        s3_bucket = app.config['S3_BUCKET_NAME']
        return f"<h1>CollabTrack MVP is Running!</h1><p>S3 Bucket Configured: <b>{s3_bucket}</b></p><p>Next: Implement User Models and Registration Route</p>"
        
    # REGISTER BLUEPRINTS (where we will put auth/project routes later) 
    # For now, we'll put the routes directly in app.py for simplicity.

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                # In a real app, you'd flash a message
                return "User already exists. Try logging in.", 409

            # Hash the password for secure storage
            # The global bcrypt object must be defined outside the function or passed in
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # Create a new user instance
            new_user = User(email=email, password_hash=hashed_password)
            
            try:
                # Add the user to the database session
                db.session.add(new_user)
                # Commit the transaction to save the user to PostgreSQL
                db.session.commit()
                
                # Success: Redirect to a confirmation or login page
                return redirect(url_for('success_page')) # We will create this route next
            except Exception as e:
                db.session.rollback() # Rollback if anything fails
                print(f"Database error during registration: {e}")
                return "Registration failed due to a database error.", 500
        
        # --- Handle GET request: Show registration form ---
        # NOTE: We are skipping HTML templates for now for simplicity, 
        # so we will just return a basic form HTML directly.
        return """
        <h1>User Registration</h1>
        <form method="POST">
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Register">
        </form>
        """

    @app.route('/success')
    def success_page():
        return "Registration successful! You can now log in (if we built that route)."
    
    @app.route('/login_test')
    def login_test():
        """TEMPORARY: Simulates a logged-in state by setting a user_id in the session."""
        
        # *** IMPORTANT: Replace 1 with the actual ID of a user you created ***
        TEST_USER_ID = 1 
        session['user_id'] = TEST_USER_ID
        session['logged_in'] = True

        # NEW: Explicitly mark the session as modified
        session.modified = True
        
        # We will manually set the session values in the code block below
        
        # Redirect to the project creation form
        return redirect(url_for('create_project'))
    
    # this route should be below the login_test route)

    @app.route('/create_project', methods=['GET', 'POST'])
    def create_project():
        # --- Check for simulated login state ---
        if 'user_id' not in session or not session.get('logged_in'):
            return "Please log in (or visit /login_test) to create a project.", 401

        owner_id = session['user_id']
        
        if request.method == 'POST':
            project_name = request.form.get('name')

            # Basic validation
            if not project_name:
                return "Project name is required.", 400

            # Create a new Project instance
            new_project = Project(name=project_name, owner_id=owner_id)
            
            try:
                # Add and commit the new project to PostgreSQL
                db.session.add(new_project)
                db.session.commit()
                
                return redirect(url_for('project_success', project_name=project_name))
            except Exception as e:
                db.session.rollback()
                print(f"Database error during project creation: {e}")
                return "Project creation failed due to a database error.", 500

        # Handle GET request: Show creation form
        return f"""
        <h1>Create New Project (Logged in as User ID: {owner_id})</h1>
        <form method="POST">
            <label for="name">Project Name:</label><br>
            <input type="text" id="name" name="name" required><br><br>
            <input type="submit" value="Create Project">
        </form>
        """
    
    @app.route('/project_success')
    def project_success():
        project_name = request.args.get('project_name', 'your new project')
        return f"Project **{project_name}** created successfully! Now ready for file uploads."

    @app.route('/upload_version', methods=['GET', 'POST'])
    def upload_version():
        # Authentication Check
        if 'user_id' not in session or not session.get('logged_in'):
            return "Please log in (or visit /login_test) to upload a version.", 401

        uploader_id = session['user_id']
        
        # Handle POST request: File Upload
        if request.method == 'POST':
            project_id = request.form.get('project_id')
            version_note = request.form.get('version_note')
            
            # Check if the post request has the file part
            if 'file' not in request.files:
                return "No file part in the request.", 400
            
            file = request.files['file']
            
            if file.filename == '':
                return "No selected file.", 400

            # Validation and File Handling 
            if file and allowed_file(file.filename):
                
                # 1. Upload to S3
                # Get configurations needed for S3
                bucket_name = app.config['S3_BUCKET_NAME']
                region = app.config['AWS_REGION']
                
                storage_key = upload_file_to_s3(
                    file_data=file, 
                    bucket_name=bucket_name, 
                    region_name=region, 
                    user_id=uploader_id, 
                    project_id=project_id
                )
                
                if not storage_key:
                    return "S3 upload failed. Check terminal logs for details.", 500
                
                # 2. Save Metadata to PostgreSQL
                
                # Simple version number logic: Find the max version number for this project
                last_version = db.session.scalar(
                    db.select(db.func.max(Version.version_number))
                      .filter_by(project_id=project_id)
                )
                # If no previous version, start at 1; otherwise, increment
                version_number = (last_version or 0) + 1
                
                new_version = Version(
                    project_id=project_id,
                    uploader_id=uploader_id,
                    version_number=version_number,
                    storage_key=storage_key,
                    file_name=secure_filename(file.filename),
                    version_note=version_note
                )
                
                try:
                    db.session.add(new_version)
                    db.session.commit()
                    return redirect(url_for('upload_success', filename=new_version.file_name, version=version_number))
                except Exception as e:
                    db.session.rollback()
                    print(f"Database error saving version metadata: {e}")
                    return "Metadata saving failed due to a database error.", 500
            
            else:
                return "File type not allowed.", 400

        # Handle GET request: Show Upload Form
        
        # NOTE: We need a list of projects for the user to select from.
        projects = Project.query.filter_by(owner_id=uploader_id).all()
        
        if not projects:
             return "Please create a project first via /create_project."
        
        # Generate the HTML form dynamically
        project_options = "".join(
            f"<option value='{p.project_id}'>{p.name}</option>" for p in projects
        )
        
        return f"""
        <h1>Upload New Version</h1>
        <form method="POST" enctype="multipart/form-data">
            <label for="project_id">Select Project:</label><br>
            <select name="project_id" required>
                {project_options}
            </select><br><br>

            <label for="file">File:</label><br>
            <input type="file" id="file" name="file" required><br><br>

            <label for="version_note">Version Note:</label><br>
            <textarea id="version_note" name="version_note"></textarea><br><br>

            <input type="submit" value="Upload Version">
        </form>
        """

    @app.route('/upload_success')
    def upload_success():
        filename = request.args.get('filename')
        version = request.args.get('version')
        return f"File **{filename}** uploaded successfully as **Version {version}**! Check your S3 bucket and database."
    
    return app

# Run the app
if __name__ == '__main__':
    # We call create_app() to run the factory function
    app = create_app()
    
    # CREATE DATABASE TABLES 
    # We use the app context to create the tables defined in our models.
    # We'll only do this once after running the SQL in DBeaver, but 
    # for a Flask-SQLAlchemy-based setup, this is a clean way to ensure tables exist.
    # NOTE: Since I manually ran the SQL in DBeaver, this is optional, 
    # but good practice for SQLAlchemy.
    with app.app_context():
        # You will need to define your Python models (users, projects, versions) 
        # before this will work as intended!
        # db.create_all() 
        print("Database initialized. You may now define your models and routes.")
        
    app.run(debug=True)