import requests

url = "https://ugv.edu.bd/portal"


payload = {
    "student_id": "12221110",
    "password": "12221110",
    "answer": "6",
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response
    print(data.text)
else:
    print("Error:", response.status_code)

    