
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from services.resume_parser import parse_resume
from services.job_matcher import match_jobs
from database.mongo_init import init_db
from models.user import User
from models.job import Job
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Initialize database
init_db(app)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to upload resume
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse the resume
        parsed_data = parse_resume(filepath)
        
        # Save user to the database
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

# Route to get job recommendations based on resume
@app.route('/get_job_recommendations', methods=['GET'])
def get_job_recommendations():
    user_id = request.args.get('user_id')
    user = User.objects(id=user_id).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    matched_jobs = match_jobs(user.skills, user.location)
    return jsonify({"recommendations": matched_jobs}), 200

if __name__ == '__main__':
    app.run(debug=True)
    