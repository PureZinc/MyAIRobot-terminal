import json
import random
from .files import datafile


class Model:
    def __init__(self, name):
        self.name = name
        self.objects = self._load_data()
    
    def _load_data(self):
        try:
            with open(datafile, "r") as f:
                return json.load(f).get(self.name, {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self):
        with open(datafile, "r") as f:
            data = json.load(f)
        
        data[self.name] = self.objects

        with open(datafile, "w") as f:
            json.dump(data, f, indent=4)

    def create(self, obj):
        obj_id = random.randint(1, 256*256)
        self.objects[obj_id] = obj
        self._save_data()
        return obj_id

    def get(self, obj_id):
        return self.objects.get(obj_id, None)

    def update(self, obj_id, new_data):
        if obj_id in self.objects:
            self.objects[obj_id].update(new_data)
            self._save_data()
            return True
        return False

    def delete(self, obj_id):
        if obj_id in self.objects:
            del self.objects[obj_id]
            self._save_data()
            return True
        return False

    def query(self, by_keys=False, **data):
        results = []
        for obj_id, obj in self.objects.items():
            if all(obj.get(key) == value for key, value in data.items()):
                results.append(obj_id) if by_keys else results.append(obj)
        return results

    def get_id(self, object):
        quer = self.query(by_keys=True, **object)
        if len(quer) != 1:
            return {}
        return quer[0]
