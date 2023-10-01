import json

class Cache:
    """
    A class for caching data as JSON in a file.

    Args:
        cache_file (str): The path to the JSON cache file.

    Attributes:
        cache_file (str): The path to the JSON cache file.
        cache (dict): The cached data stored as a dictionary.

    Methods:
        load_cache(): Load cached data from the JSON file.
        save_cache(): Save the current cache data to the JSON file.
        get_data(url): Get cached data for a specific URL.
        set_data(url, data): Set and save cached data for a specific URL.
    """

    def __init__(self, cache_file):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """
        Load cached data from the JSON file.

        Returns:
            dict: The cached data as a dictionary.
        """
        try:
            with open(self.cache_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_cache(self):
        """
        Save the current cache data to the JSON file.
        """
        with open(self.cache_file, 'w') as file:
            json.dump(self.cache, file)

    def get_data(self, url):
        """
        Get cached data for a specific URL.

        Args:
            url (str): The URL for which to retrieve cached data.

        Returns:
            dict or None: The cached data for the URL, or None if not found.
        """
        return self.cache.get(url, None)

    def set_data(self, url, data):
        """
        Set and save cached data for a specific URL.

        Args:
            url (str): The URL for which to set cached data.
            data (dict): The data to be cached for the URL.
        """
        self.cache[url] = data
        self.save_cache()
