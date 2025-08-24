import json

def readDB(path):
    try:
        with open(path, "r") as file:
            # db = file.read()
            return json.load(file)
    except Exception as e:
        print(f'ERROR: ${e}')
        return None

def writeDB(path, data):
    try:
        with open(path, "w") as file:
            file.write(json.dumps(data))
    except Exception as e:
        print(f'ERROR: ${e}')

