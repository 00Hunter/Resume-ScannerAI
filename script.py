import requests

API_KEY = "AIzaSyCR9xEY8duCyig0FWsRBaBBowlthc4kGic"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

headers = {"Content-Type": "application/json"}
data = {
    "contents": [{"parts": [{"text": "what is 2+2 in words and who is president of india also correct spelling of Inida"}]}]
}

response = requests.post(URL, json=data, headers=headers)
print(response.json())
