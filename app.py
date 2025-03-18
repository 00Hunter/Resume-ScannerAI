import json
import time
import os


from flask import Flask, request, Response,jsonify
from resume_extraction import parse_resume
from resume_extraction import calculate_resume_score
from improve_gemini import improve_resume_gemini
from response_process import process_response
from celery import Celery
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "resume_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def analyze_resume_task(resume_text, job_desc):
    """ Asynchronous task to generate AI analysis """
    time.sleep(2)  # Simulate processing delay
    improvement_suggestions =  improve_resume_gemini(resume_text, job_desc)
    return {"improvements": improvement_suggestions}


# @app.route('/upload', methods=['POST'])
# def upload_resume():
#     # if 'resume' not in request.files:
#     #     return jsonify({"error": "No file uploaded"}), 400

#     resume_text=parse_resume();
#     job_desc = request.form.get("job_description", "")

#     if not job_desc:
#         return jsonify({"error": "Job description required"}), 400

#     score = calculate_resume_score(job_desc)
#     print("score",score)
#     # return jsonify({"score": score, "message": f"Resume matches {score}% with job description"})
#     improvement_suggestions = improve_resume_gemini(resume_text, job_desc)
#     result=process_response(improvement_suggestions)
#     # print(result)
#     cleaned_response = improvement_suggestions.strip('"')
#     return Response(improvement_suggestions, status=200, mimetype='text/markdown')
@app.route('/upload', methods=['POST'])
def upload_resume():

    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    job_desc = request.form.get("job_description", "")

    if not job_desc:
        return Response("Error: Job description required", status=400, mimetype='text/plain')

    resume_file = request.files['resume']
    if resume_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not resume_file.filename.endswith(".pdf"):
        return jsonify({"error": "Invalid file format. Please upload a PDF."}), 400

    file_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(file_path) 

    resume_text = parse_resume(file_path)
   

    score = calculate_resume_score(resume_text,job_desc)
    # print(score)
    task = analyze_resume_task.apply_async(args=[resume_text, job_desc])

    return jsonify({"task_id": task.id, "status": "processing", "score": score})

@app.route('/task-status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = analyze_resume_task.AsyncResult(task_id)
    print(task)

    if task.state == 'PENDING':
        return jsonify({"status": "processing"})
    elif task.state == 'SUCCESS':
        return jsonify({"status": "completed", "improvements": task.result})
    else:
        return jsonify({"status": "error", "message": "Task failed"}), 500

       
if __name__ == '__main__':
    app.run(debug=True)
