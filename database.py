import json
from time import sleep

def database():
    while True:
        with open("database.json", "w") as json_file:
            data = [{"Name":"Fred"}]
            json.dumps(data, json_file)
            sleep(0.5)
