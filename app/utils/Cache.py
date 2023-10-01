import json

class Cache:
    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.cache_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_cache(self):
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file)

    def get_data(self, url):
        return self.cache.get(url, None)

    def set_data(self, url, data):
        self.cache[url] = data
        self.save_cache()