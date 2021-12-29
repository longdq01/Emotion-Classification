import requests
import json

response = requests.post('http://localhost:5000/post',
                         json={'id': 1, 'name': 'Jessa'})

print("Status code: ", response.status_code)
print("Printing Entire Post Request")
print(response.json())
