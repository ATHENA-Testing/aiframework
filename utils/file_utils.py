import json
import os
import yaml

class FileUtils:
    @staticmethod
    def read_json(path):
        with open(path, 'r') as f:
            return json.load(f)

    @staticmethod
    def read_yaml(path):
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_json(path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def ensure_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)
