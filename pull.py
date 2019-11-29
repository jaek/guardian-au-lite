from config import api_url
from secrets import api_key
import requests
import subprocess
from markdownify import markdownify as md

class Guardian_request():
    def __init__(self, api_url, api_key):
        self.articles = {}
        self.api_url = api_url
        self.headers = {"api-key": api_key, "format":"json"} 

    def get_latest(self, n="15"):
        response = requests.get(self.api_url+n, self.headers)
        for r in response.json()["response"]["results"]:
            self.articles[r["webTitle"]] = self.clean_article(r["blocks"]["body"][0]["bodyHtml"])

    def print_article_titles(self):
        for title in self.articles:
            print(title)

    def download_articles(self, dir="./articles/"):
        i = 0
        with open(f"{dir}index.md", "w+") as f1: 
            for article in self.articles:
                with open(f"{dir}{i}.md", "w+") as f2:
                    f1.write(f"{i}. {article}\n\n")
                    f2.write(f"## {article}")
                    f2.write(self.articles[article])
                i = i + 1

    def clean_article(self, html):
        s = md(html, strip=['a'])
        return s

    def show_index(self):
        while(True):
            i = 0
            for title in self.articles:
                 print(f"{i}. {title}")
                 i += 1
            print("CTRL-D to exit.")
            n = input(f"Show which article (0-{i})")        
            if(n == "q"):
                exit()
            elif(int(n) < 0 or int(n) > i):
                print("ERROR: Please enter a number\n****\n")
            else:
                subprocess.run(["mdless", f"./articles/{n}.md"])
        
if __name__ == "__main__":
    g = Guardian_request(api_url, api_key)
    g.get_latest()
    g.download_articles()
    g.show_index()
