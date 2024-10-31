import json
import random
from config.config import datafile


class Model:
    def __init__(self, name: str):
        self.name = name
        self.data = self._load_data()
        self.objects = self._get_list_data()
    
    def _get_list_data(self) -> list:
        return [{"id": obj_id, **obj} for obj_id, obj in self.data.items()]
    
    def _load_data(self) -> dict:
        try:
            with open(datafile, "r") as f:
                return json.load(f).get(self.name, {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self):
        with open(datafile, "r") as f:
            data = json.load(f)
        
        data[self.name] = self.data

        with open(datafile, "w") as f:
            json.dump(data, f, indent=4)

    def create(self, obj):
        obj_id = random.randint(1, 256*256)
        self.data[obj_id] = obj
        self._save_data()
        return obj_id

    def get(self, obj_id):
        return self.data.get(obj_id, None)

    def update(self, obj_id, new_data):
        if obj_id in self.objects:
            self.data[obj_id].update(new_data)
            self._save_data()
            return True
        return False

    def delete(self, obj_id):
        if obj_id in self.objects:
            del self.data[obj_id]
            self._save_data()
            return True
        return False

    def query(self, **data):
        results = []
        for obj in self.objects:
            if all(obj[data_key] == data_value for data_key, data_value in data.items()):
                results.append(obj)
        return results

    def get_id(self, object):
        quer = self.query(by_keys=True, **object)
        if len(quer) != 1:
            return {}
        return quer[0]
