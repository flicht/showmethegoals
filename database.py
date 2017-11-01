import json
from time import sleep

def database():


    with open("app/database.json", "r+w") as json_file:

        data = [{"Name":"Fred"}]
        json.dumps(data, json_file)
        sleep(0.5)


if __name__ == "__main__":
    database()
