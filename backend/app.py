from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from services.resume_parser import parse_resume
from services.job_matcher import match_jobs
from database.mongo_init import init_db
from models.user import User
from models.job import Job
import os

# Create Flask app with static folder set
app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Initialize database
init_db(app)

# Serve index.html at root URL
@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

# Allow only specific file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Resume upload API
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        parsed_data = parse_resume(filepath)
        new_user = User(
            name=parsed_data['name'],
            email=request.form['email'],
            skills=parsed_data['skills'],
            location=parsed_data['location'],
            resume_path=filepath
        )
        new_user.save()

        return jsonify({"message": "Resume uploaded and parsed", "data": parsed_data}), 200

    return jsonify({"message": "Invalid file type"}), 400

# Job recommendations API
@app.route('/get_job_recommendations', methods=['GET'])
def get_job_recommendations():
    user_id = request.args.get('user_id')
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    matched_jobs = match_jobs(user.skills, user.location)
    return jsonify({"recommendations": matched_jobs}), 200

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
