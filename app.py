from flask import Flask, request, jsonify, send_from_directory
from flask_mail import Mail, Message
from models import db, User, File
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)


app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        file_path = save_file(file, app.config['UPLOAD_FOLDER'])
        return jsonify({'message': 'File uploaded successfully', 'path': file_path}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/login', methods=['POST'])
def login():
    # Login logic for Ops User (use Flask-Login or basic authentication)
    pass

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Store file info in database
        new_file = File(filename=filename, file_url=os.path.join(UPLOAD_FOLDER, filename), user_id=1)  # Ops User
        db.session.add(new_file)
        db.session.commit()
        return jsonify({'message': 'File uploaded successfully'})
    else:
        return jsonify({'message': 'Invalid file type'}), 400

@app.route('/signup', methods=['POST'])
def signup():
    # Signup logic for Client User, send verification email with encrypted URL
    pass

@app.route('/email-verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        user_id = s.loads(token, salt='email-verify', max_age=3600)  # 1 hour expiry
        user = User.query.get(user_id)
        user.is_verified = True
        db.session.commit()
        return jsonify({'message': 'Email verified successfully'}), 200
    except:
        return jsonify({'message': 'Invalid or expired token'}), 400

@app.route('/download-file/<file_id>', methods=['GET'])
def download_file(file_id):
    # Validate that the request is from a Client User
    if not current_user.is_client:
        return jsonify({'message': 'Unauthorized'}), 403
    try:
        file = File.query.get(file_id)
        if file:
            encrypted_url = generate_encrypted_url(file_id)
            return jsonify({'download-link': encrypted_url, 'message': 'success'})
        return jsonify({'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

from flask_login import LoginManager
