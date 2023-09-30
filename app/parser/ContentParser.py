from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class ContentParser:
    def __init__(self, url):
        self.url = url
        self.html_content = None
        self.content = ""

    def set_url(self, url):
        self.url = url

    def fetch_content(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(self.url)
            self.html_content = driver.page_source
            driver.quit()
        except Exception as e:
            print(f"Error fetching URL {self.url} with Selenium: {str(e)}")

    def parse_content(self):
        if self.html_content:
            soup = BeautifulSoup(self.html_content, 'html.parser')
            divs = soup.find_all('div')
            for div in divs:
                if not div.find_all('div'):
                    text = div.get_text(strip=True)
                    if text:
                        self.content += text + '\n'
        # self.content = self.content[2000:]

    def reset(self):
        self.content = ""
        self.url = ""
        self.html_content = ""


if __name__ == "__main__":
    url = "https://megamarket.ru/catalog/audiosistemy-dlya-lodok-i-katerov/"
    parser = ContentParser(url)
    parser.fetch_content()
    parser.parse_content()

    print(f"URL: {parser.url}")
    print(f"Content:\n{parser.content}")
