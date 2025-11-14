from database import db
from datetime import datetime

class User(db.Model):
    """
    Maps to the 'users' table. Used for authentication and linking ownership.
    """
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define the relationship to Projects (not a column, but a SQLAlchemy feature)
    projects = db.relationship('Project', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.email}')"

class Project(db.Model):
    """
    Maps to the 'projects' table. Stores project metadata.
    """
    __tablename__ = 'projects'
    
    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Foreign Key linking to User
    owner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define the relationship to Versions
    versions = db.relationship('Version', backref='project', lazy=True)

    def __repr__(self):
        return f"Project('{self.name}', Owner: {self.owner_id})"


class Version(db.Model):
    """
    Maps to the 'versions' table. Stores metadata about the uploaded files/versions.
    """
    __tablename__ = 'versions'
    
    version_id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    version_number = db.Column(db.Integer, nullable=False)
    storage_key = db.Column(db.String(512), unique=True, nullable=False) # The path in S3
    file_name = db.Column(db.String(255), nullable=False)
    version_note = db.Column(db.Text)
    attestation_status = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to the Uploader
    uploader = db.relationship('User', foreign_keys=[uploader_id], backref='uploaded_versions', lazy=True)

    def __repr__(self):
        return f"Version('{self.file_name}', v{self.version_number})"