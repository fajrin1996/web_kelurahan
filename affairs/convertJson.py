import json, csv

json_path = "RekAir.json"
csv_path = "../titanic.csv"

jsonData = {}

with open(csv_path, encoding='utf-8') as csvfile:
    csvData = csv.DictReader(csvfile)
    for rows in csvData:
        key = rows['PassengerId']
        jsonData[key]=rows

with open(json_path, 'w', encoding='utf-8') as jsonFile:
    jsonFile.write(json.dumps(jsonData, indent=4))

    