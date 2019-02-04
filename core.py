import requests
from bs4 import BeautifulSoup
import time
import difflib
import shutil


class Scraper(object):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 " \
         "Safari/537.36"

    state = ""

    def __init__(self, logger, url, path, email, frequency=60):
        self.logger = logger
        self.url = url
        self.path = path
        self.email = email
        self.frequency = set_frequency(frequency)

    def run(self):
        self.logger.info('Running on ' + self.url + ', freq=' + self.frequency.__str__())
        changed = False

        while not changed:  # todo
            self.logger.info("Scraping...")
            changed = self.scrape()

            if changed:
                self.logger.info("CHANGES DETECTED")
            else:
                self.logger.info('No changes')
                time.sleep(60)

    def scrape(self):
        soup = self.__download__()
        [s.extract() for s in soup("script")]  # removing script tags
        soup = soup.prettify()

        self.logger.info("Creating new.html")
        with open(self.path + "/resources/new.html", "w") as f:
            f.write(soup)

        if not self.state:
            self.logger.info("Creating state.html")
            shutil.copy2(self.path + "/resources/new.html", self.path + "/resources/state.html")
            self.state = soup

        diff = self.compare(soup)
        # with open("../diff.html", "w") as f:
        #     f.write(diff)

        return diff

    def compare(self, new):
        new_lines = new.splitlines()
        state_lines = self.state.splitlines()

        d = difflib.Differ()
        diff = d.compare(state_lines, new_lines)
        diff = [line for line in diff if str.startswith(line, ("+", "-"))]

        if diff:
            diff_html = difflib.HtmlDiff().make_table(state_lines, new_lines)

            self.logger.info("Creating diff.html")
            with open(self.path + "/resources/diff.html", "w") as f:
                f.write(diff_html)

        self.logger.info("Rewriting state")
        self.state = new
        with open(self.path + "/resources/state.html", "w") as f:
            f.write(self.state)

        return diff

    def __download__(self):
        self.logger.info("Downloading source code...")
        headers = {"User-Agent": self.ua}
        response = requests.get(self.url, headers=headers)
        return BeautifulSoup(response.text, "html.parser")


def set_frequency(f):
    return f if f and 30 <= f <= 86400 else 60


def main(logger, path, url, email, frequency=60):
    if not url:
        url = 'https://web-daemon.weebly.com'

    sc = Scraper(logger, url, path, email, frequency)
    sc.run()
