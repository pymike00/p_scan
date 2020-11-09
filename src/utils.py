import json

PORTS_DATA_FILE = "./common_ports.json"


def extract_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def get_ports():
    data = extract_json_data(PORTS_DATA_FILE)
    return {int(k): v for (k, v) in data.items()}


if __name__ == "__main__":
    print(get_ports())