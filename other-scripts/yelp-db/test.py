import json

file = open('./yelp-db/yelp.json')

data = json.load(file)

print(data.keys())

print(data['businesses'][0].keys())