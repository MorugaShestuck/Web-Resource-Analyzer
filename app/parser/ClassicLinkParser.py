import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class ClassicLinkParser:
    """
    A class for parsing links from web pages using a classic crawling approach.

    Args:
        headers (dict, optional): HTTP headers to use in requests. Defaults to a common User-Agent header.

    Attributes:
        headers (dict): HTTP headers for requests.
        site_links (list): A list to store the parsed website links.
        type (str): The type of link parser, which is set to "Classic" by default.

    Methods:
        crawl(start_url, max_pages=10): Crawl web pages starting from a given URL, up to a specified maximum number of pages.
        print(): Print the parsed website links.
        clear(): Clear the list of parsed links.
        get(index): Get a link at a specific index in the parsed links list.
        remove(index): Remove a link at a specific index from the parsed links list.
        length(): Get the number of parsed links in the list.
    """

    def __init__(self, headers=None):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.site_links = []
        self.type = "Classic"

    def crawl(self, start_url, max_pages=10):
        """
        Crawl web pages starting from a given URL, up to a specified maximum number of pages.

        Args:
            start_url (str): The starting URL for crawling.
            max_pages (int, optional): The maximum number of pages to crawl. Defaults to 10.
        """
        visited_urls, pages_to_visit = set(), [start_url]

        while pages_to_visit and len(self.site_links) < max_pages:
            url = pages_to_visit.pop(0)
            if url in visited_urls:
                continue
            visited_urls.add(url)
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href, abs_url = link['href'], urljoin(url, link['href'])
                        if abs_url not in visited_urls and abs_url not in self.site_links:
                            pages_to_visit.append(abs_url)
                            self.site_links.append(abs_url)
            except Exception as e:
                print(f"Error fetching URL {url}: {str(e)}")

    def print(self):
        """Print the parsed website links."""
        for link in self.site_links:
            print(link)

    def clear(self):
        """Clear the list of parsed links."""
        self.site_links = []

    def get(self, index):
        """
        Get a link at a specific index in the parsed links list.

        Args:
            index (int): The index of the link to retrieve.

        Returns:
            str or None: The link at the specified index or None if the index is out of bounds.
        """
        if 0 <= index < len(self.site_links):
            return self.site_links[index]
        else:
            return None

    def remove(self, index):
        """
        Remove a link at a specific index from the parsed links list.

        Args:
            index (int): The index of the link to remove.
        """
        if 0 <= index < len(self.site_links):
            self.site_links.pop(index)

    def length(self):
        """
        Get the number of parsed links in the list.

        Returns:
            int: The number of parsed links.
        """
        return len(self.site_links)
