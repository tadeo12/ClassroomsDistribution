import json
import os

class ConfigManager:
    _instance = None  # Singleton

    def __new__(cls, path="config.json"):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, path="config.json"):
        if self._initialized:
            return
        self.path = path
        self.config = {}
        self.load()
        self._initialized = True

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=2)

    def getConfig(self):
        return self.config

    def updateConfig(self, newConfig):
        self.config.update(newConfig)
        self.save()

