import json

from flask import Flask, request, Response
from resume_extraction import parse_resume
from resume_extraction import calculate_resume_score
from improve_gemini import improve_resume_gemini
from response_process import process_response


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_resume():
    # if 'resume' not in request.files:
    #     return jsonify({"error": "No file uploaded"}), 400

    resume_text=parse_resume();
    job_desc = request.form.get("job_description", "")

    if not job_desc:
        return jsonify({"error": "Job description required"}), 400

    score = calculate_resume_score(job_desc)
    print("score",score)
    # return jsonify({"score": score, "message": f"Resume matches {score}% with job description"})
    improvement_suggestions = improve_resume_gemini(resume_text, job_desc)
    result=process_response(improvement_suggestions)
    # print(result)
    cleaned_response = improvement_suggestions.strip('"')
    return Response(improvement_suggestions, status=200, mimetype='text/markdown')
       
if __name__ == '__main__':
    app.run(debug=True)
