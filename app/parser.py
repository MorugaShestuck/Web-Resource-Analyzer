import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def crawl(start_url, max_pages=10):
    visited, to_visit, crawled = set(), [start_url], []

    while to_visit and len(crawled) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            r = requests.get(url)
            visited.add(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href, abs_url = link['href'], urljoin(url, link['href'])
                    if abs_url not in visited:
                        to_visit.append(abs_url)
                crawled.append({'url': url, 'content': r.text})
        except Exception as e:
            print(f"Error fetching URL {url}: {str(e)}")
    return crawled


# if __name__ == "__main__":
#     start_url, max_pages = "https://pet-mir.ru/", 10
#     crawled_data = crawl(start_url, max_pages)
#     for data in crawled_data:
#         print(data)

