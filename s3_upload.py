import boto3
from flask import current_app # Used to get config variables from the running app
import os
from werkzeug.utils import secure_filename
import uuid

def upload_file_to_s3(file_data, bucket_name, region_name, user_id, project_id):
    """
    Uploads a file to an S3 bucket and returns the unique storage key (S3 path).
    
    Args:
        file_data (FileStorage): The file object from Flask's request.files.
        bucket_name (str): The name of the S3 bucket.
        region_name (str): The AWS region of the bucket.
        user_id (int): The ID of the user uploading the file.
        project_id (int): The ID of the project the file belongs to.
        
    Returns:
        str or None: The unique S3 storage key (path) if successful, None otherwise.
    """
    
    # 1. Initialize S3 client
    try:
        s3_client = boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY']
        )
    except Exception as e:
        print(f"ERROR: Could not initialize Boto3 client: {e}")
        return None

    # 2. Generate a unique, structured storage key (path)
    # Format: projects/{project_id}/{user_id}-{unique_id}-{filename}
    filename = secure_filename(file_data.filename)
    unique_file_id = str(uuid.uuid4())
    
    storage_key = os.path.join(
        'projects',
        str(project_id),
        f'{user_id}-{unique_file_id}-{filename}'
    ).replace('\\', '/') # Ensure forward slashes for S3 paths

    # 3. Upload the file
    try:
        # Move the cursor back to the start of the file before uploading
        file_data.seek(0)
        
        s3_client.upload_fileobj(
            file_data,
            bucket_name,
            storage_key
        )
        # Return the unique path used to retrieve the file later
        return storage_key
        
    except Exception as e:
        print(f"ERROR: S3 Upload failed for {filename}: {e}")
        return None


def allowed_file(filename):
    """A basic function to validate file extensions."""
    # Define a simple set of allowed extensions for the MVP
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dwg', 'dxf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS