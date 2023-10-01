from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class ContentParser:
    """
    A class for parsing content from a web page using Selenium and BeautifulSoup.

    Args:
        url (str): The URL of the web page to parse.

    Attributes:
        url (str): The URL of the web page to parse.
        html_content (str): The HTML content of the web page.
        content (str): The parsed text content of the web page.

    Methods:
        set_url(url): Set the URL of the web page.
        fetch_content(): Fetch the HTML content of the web page using Selenium.
        parse_content(): Parse the text content from the HTML using BeautifulSoup.
        reset(): Reset the content parser's attributes.
    """

    def __init__(self, url):
        self.url = url
        self.html_content = None
        self.content = ""

    def set_url(self, url):
        """
        Set the URL of the web page to parse.

        Args:
            url (str): The URL of the web page.
        """
        self.url = url

    def fetch_content(self):
        """
        Fetch the HTML content of the web page using Selenium and Chrome WebDriver.
        """
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
        """
        Parse the text content from the HTML using BeautifulSoup.
        """
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
        """
        Reset the content parser's attributes.
        """
        self.content = ""
        self.url = ""
        self.html_content = ""
