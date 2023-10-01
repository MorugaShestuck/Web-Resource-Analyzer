import hashlib
from app.utils.hash_table import HashTable
from app.parser.ContentParser import ContentParser
import openpyxl


class Analyzer:
    def __init__(self, keywords, url=""):
        self.keywords = keywords
        self.url = url
        self.score = {}
        self.frequent_keywords = {}

    def set_url(self, url):
        self.url = url

    def analyze_content(self, content):
        for keyword, topic in self.keywords:
            count = content.lower().count(keyword.lower())
            if topic not in self.score:
                self.score[topic] = 0
            self.score[topic] += count

            if count > 0:
                if keyword not in self.frequent_keywords:
                    self.frequent_keywords[keyword] = 0
                self.frequent_keywords[keyword] += count

    def get_score(self, deep=None):
        sorted_keywords = sorted(self.score.items(), key=lambda x: x[1], reverse=True)

        if deep is None:
            return {k: v for k, v in sorted_keywords if v > 0}
        else:
            result = {}
            count = 0
            for k, v in sorted_keywords:
                if v > 0:
                    result[k] = v
                    count += 1
                    if count >= deep:
                        break
            return result

    def get_frequent_keywords(self):
        sorted_keywords = sorted(self.frequent_keywords.items(), key=lambda x: x[1], reverse=True)
        return {k: v for k, v in sorted_keywords if v > 0}

    def reset(self):
        self.score = {}
        self.frequent_keywords = {}

    def get_url(self):
        return self.url

    def load_keywords(self, keywords):
        self.keywords = keywords


if __name__ == "__main__":
    keywords = HashTable()
    keywords.load("data.json")
    file_path = '../data/sites.xlsx'
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook['Лист1']
    column_data = []
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=1, values_only=True):
        cell_value = row[0]
        column_data.append(cell_value)
    workbook.close()

    for link in column_data:
        p = ContentParser(url=link)
        a = Analyzer(keywords=keywords)
        p.fetch_content()
        p.parse_content()
        a.analyze_content(p.content)
        print(link)
        print(a.get_score())
        print(a.get_frequent_keywords())
        p.reset()
        a.reset()
        print("\n")
