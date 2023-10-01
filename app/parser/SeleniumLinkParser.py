from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class SeleniumLinkParser:
    """
    A class for parsing links from web pages using Selenium and Chrome WebDriver.

    Args:
        driver_path (str): The path to the Chrome WebDriver executable (optional).

    Attributes:
        driver_path (str): The path to the Chrome WebDriver executable.
        site_links (list): A list of parsed links.
        type (str): The type of link parser (Selenium).

    Methods:
        get_content(url): Fetch the HTML content of a web page using Selenium.
        crawl(start_url, max_pages=10): Crawl web pages to extract links.
        print(): Print the parsed links.
        clear(): Clear the list of parsed links.
        get(index): Get a link from the list by index.
        remove(index): Remove a link from the list by index.
        length(): Get the number of parsed links.
    """

    def __init__(self, driver_path=""):
        self.driver_path = driver_path
        self.site_links = []
        self.type = "Selenium"

    def get_content(self, url):
        """
        Fetch the HTML content of a web page using Selenium and Chrome WebDriver.

        Args:
            url (str): The URL of the web page.

        Returns:
            str: The HTML content of the web page.
        """
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        html_content = driver.page_source
        driver.quit()
        self.site_links.clear()
        return html_content

    def crawl(self, start_url, max_pages=10):
        """
        Crawl web pages to extract links.

        Args:
            start_url (str): The starting URL for crawling.
            max_pages (int): The maximum number of pages to crawl (default is 10).
        """
        visited_urls, pages_to_visit = set(), [start_url]

        while pages_to_visit and len(self.site_links) < max_pages:
            url = pages_to_visit.pop(0)
            if url in visited_urls:
                continue
            visited_urls.add(url)
            try:
                html_content = self.get_content(url)
                soup = BeautifulSoup(html_content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href, abs_url = link['href'], urljoin(url, link['href'])
                    if abs_url not in visited_urls and abs_url not in self.site_links:
                        pages_to_visit.append(abs_url)
                        self.site_links.append(abs_url)
            except Exception as e:
                print(f"Error fetching URL {url}: {str(e)}")

    def print(self):
        """
        Print the parsed links.
        """
        for link in self.site_links:
            print(link)

    def clear(self):
        """
        Clear the list of parsed links.
        """
        self.site_links.clear()

    def get(self, index):
        """
        Get a link from the list by index.

        Args:
            index (int): The index of the link to retrieve.

        Returns:
            str: The link at the specified index or None if index is out of range.
        """
        if 0 <= index < len(self.site_links):
            return self.site_links[index]
        else:
            return None

    def remove(self, index):
        """
        Remove a link from the list by index.

        Args:
            index (int): The index of the link to remove.
        """
        if 0 <= index < len(self.site_links):
            del self.site_links[index]

    def length(self):
        """
        Get the number of parsed links.

        Returns:
            int: The number of parsed links.
        """
        return len(self.site_links)
