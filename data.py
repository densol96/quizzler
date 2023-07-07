import requests


trivia_api_endpoint = "https://opentdb.com/api.php"

parameters = {
    "amount": 10,
    "type": "boolean"
}

response = requests.get(url=trivia_api_endpoint, params=parameters)
response.raise_for_status()

data = response.json() #is a dictionary with 2 keys: "response code" and "results"
question_data = data["results"] #a list of quiz questions dictionaries

print(question_data)