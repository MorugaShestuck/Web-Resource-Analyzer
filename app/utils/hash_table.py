import hashlib
import json


class HashTable:
    """
    A hash table (dictionary) implementation with support for resizing.

    Args:
        initial_size (int): The initial size of the hash table.
        load_factor (float): The load factor that triggers resizing.

    Attributes:
        size (int): The current size of the hash table.
        buckets (list): A list of buckets where each bucket is a list of key-value pairs.
        load_factor (float): The load factor that triggers resizing.
        num_elements (int): The number of elements currently in the hash table.

    Methods:
        _hash(key): Hashes a key to find the index in the buckets.
        _resize(): Resizes the hash table when load factor is exceeded.
        insert(key, value): Inserts a key-value pair into the hash table.
        get(key): Retrieves the value associated with a given key.
        delete(key): Deletes a key-value pair based on the key.
        load(json_file): Loads data from a JSON file into the hash table.
        save(json_file): Saves the hash table data into a JSON file.
        __iter__(): Iterates over the key-value pairs in the hash table.
    """

    def __init__(self, initial_size=1000, load_factor=0.7):
        self.size = initial_size
        self.buckets = [[] for _ in range(initial_size)]
        self.load_factor = load_factor
        self.num_elements = 0

    def _hash(self, key):
        """
        Hashes a key to find the index in the buckets.

        Args:
            key (str): The key to be hashed.

        Returns:
            int: The index in the buckets.
        """
        hash_object = hashlib.sha256(key.encode())
        return int(hash_object.hexdigest(), 16) % self.size

    def _resize(self):
        """
        Resizes the hash table when load factor is exceeded.
        """
        self.size *= 2
        new_buckets = [[] for _ in range(self.size)]

        for bucket in self.buckets:
            for key, value in bucket:
                index = self._hash(key)
                new_buckets[index].append((key, value))

        self.buckets = new_buckets

    def insert(self, key, value):
        """
        Inserts a key-value pair into the hash table.

        Args:
            key (str): The key to be inserted.
            value: The value associated with the key.
        """
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
        """
        Retrieves the value associated with a given key.

        Args:
            key (str): The key for which to retrieve the value.

        Returns:
            value: The value associated with the key.

        Raises:
            KeyError: If the key is not found in the hash table.
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        """
        Deletes a key-value pair based on the key.

        Args:
            key (str): The key to be deleted.

        Raises:
            KeyError: If the key is not found in the hash table.
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.num_elements -= 1
                return
        raise KeyError(f"Key '{key}' not found")

    def load(self, json_file):
        """
        Loads data from a JSON file into the hash table.

        Args:
            json_file (str): The path to the JSON file.

        Raises:
            FileNotFoundError: If the JSON file is not found.
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for key, value in data.items():
                    self.insert(key, value)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{json_file}' not found")

    def save(self, json_file):
        """
        Saves the hash table data into a JSON file.

        Args:
            json_file (str): The path to the JSON file.
        """
        data = {}
        for bucket in self.buckets:
            for key, value in bucket:
                data[key] = value
        with open(json_file, 'w') as file:
            json.dump(data, file)

    def __iter__(self):
        """
        Iterates over the key-value pairs in the hash table.

        Yields:
            Tuple[str, value]: A tuple containing the key and value.
        """
        for bucket in self.buckets:
            for key, value in bucket:
                yield key, value

