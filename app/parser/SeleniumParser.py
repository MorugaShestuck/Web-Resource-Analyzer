from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class SeleniumParser:
    def __init__(self, driver_path=""):
        self.driver_path = driver_path
        self.site_links = []
        self.type = "Selenium"

    def get_content(self, url):
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
        for link in self.site_links:
            print(link)

    def clear(self):
        self.site_links.clear()

    def get(self, index):
        if 0 <= index < len(self.site_links):
            return self.site_links[index]
        else:
            return None

    def remove(self, index):
        if 0 <= index < len(self.site_links):
            del self.site_links[index]

    def length(self):
        return len(self.site_links)


if __name__ == "__main__":
    start_url, max_depth = "https://pet-mir.ru/", 3

    parser = SeleniumParser()
    parser.crawl(start_url, max_depth)
    parser.print()
    print(parser.length())
