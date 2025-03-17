import requests

# Replace with your actual Gemini API key
GEMINI_API_KEY = "AIzaSyCR9xEY8duCyig0FWsRBaBBowlthc4kGic"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def improve_resume_gemini(resume_text, job_desc):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{
                "text": f"Here is a resume:\n{resume_text}\n\n"
                        f"Here is a job description:\n{job_desc}\n\n"
                        f"Suggest improvements to make this resume a better match for the job description.return only the **missing keywords** and **key areas for improvement**"
            }]
        }]
    }
    
    response = requests.post(GEMINI_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Error: Unexpected response from Gemini API."
    else:
        return f"Error: {response.status_code}, {response.text}"
