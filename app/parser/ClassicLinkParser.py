import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class ClassicLinkParser:
    def __init__(self, headers=None):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.site_links = []
        self.type = "Classic"

    def crawl(self, start_url, max_pages=10):
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
        for link in self.site_links:
            print(link)

    def clear(self):
        self.site_links = []

    def get(self, index):
        if 0 <= index < len(self.site_links):
            return self.site_links[index]
        else:
            return None

    def remove(self, index):
        if 0 <= index < len(self.site_links):
            self.site_links.pop(index)

    def length(self):
        return len(self.site_links)


if __name__ == "__main__":
    start_url, max_pages = "https://pet-mir.ru/", 3
    parser = ClassicParser()
    parser.crawl(start_url, max_pages)

    print("Total links count:", parser.length())
    parser.print()
