import os
import secrets
from werkzeug.utils import secure_filename

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}

# Check if a file extension is allowed
def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Generate a secure, random token for URLs
def generate_secure_token(length=24):
    return secrets.token_urlsafe(length)

# Securely save an uploaded file
def save_file(file, upload_folder):
    if is_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    else:
        raise ValueError("File type not allowed.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_encrypted_url(file_id):
    return s.dumps(file_id, salt='file-download')
