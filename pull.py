from config import api_url
from secrets import api_key
import requests
from markdownify import markdownify as md

class Guardian_request():
    def __init__(self, api_url, api_key):
        self.articles = {}
        self.api_url = api_url
        self.headers = {"api-key": api_key, "format":"json"} 

    def get_latest(self, n="30"):
        response = requests.get(self.api_url+n, self.headers)
        for r in response.json()["response"]["results"]:
           self.articles[r["webTitle"]] = self.clean_article(r["blocks"]["body"][0]["bodyHtml"])

    def print_article_titles(self):
        for title in self.articles:
            print(title)

    def article_to_file(self):
        i = 0
        for article in self.articles:
            with open(f"{i}.md", "w+") as f:
                f.write(f"## {article}")
                f.write(self.articles[article])
                i = i + 1

    def clean_article(self, html):
        s = md(html, strip=['a'])
        return s

g = Guardian_request(api_url, api_key)
g.get_latest()
g.article_to_file()
