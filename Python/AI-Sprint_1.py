import json

data = {}

with open('steam.json', 'r') as json_file:
    data = json.load(json_file)

def eersteNaam():
    print(f'De naam van het eerste spel is: {data[0]["name"]}')

eersteNaam()