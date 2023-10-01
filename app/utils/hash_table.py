import hashlib
import json


class HashTable:
    def __init__(self, initial_size=1000, load_factor=0.7):
        self.size = initial_size
        self.buckets = [[] for _ in range(initial_size)]
        self.load_factor = load_factor
        self.num_elements = 0

    def _hash(self, key):
        hash_object = hashlib.sha256(key.encode())
        return int(hash_object.hexdigest(), 16) % self.size

    def _resize(self):
        self.size *= 2
        new_buckets = [[] for _ in range(self.size)]

        for bucket in self.buckets:
            for key, value in bucket:
                index = self._hash(key)
                new_buckets[index].append((key, value))

        self.buckets = new_buckets

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.num_elements += 1

        if self.num_elements / self.size > self.load_factor:
            self._resize()

    def get(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.num_elements -= 1
                return
        raise KeyError(f"Key '{key}' not found")

    def load(self, json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    self.insert(key, value)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{json_file}' not found")

    def save(self, json_file):
        data = {}
        for bucket in self.buckets:
            for key, value in bucket:
                data[key] = value
        with open(json_file, 'w') as file:
            json.dump(data, file)

    def __iter__(self):
        for bucket in self.buckets:
            for key, value in bucket:
                yield key, value


if __name__ == "__main__":
    h = HashTable()
    h.load("../data/categories.json")
    print(h.get("Ремонт"))
