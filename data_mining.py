import requests
import json
from pathlib import Path
import time

url = 'https://5ka.ru/api/v2/special_offers/'


class Parser5ka:
    headers = {"User-Agent": 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/86.0.4240.198 Safari/537.36"}

    def __init__(self, start_url):
        self.start_url = start_url


    def run(self):
        for product in self.parse(self.start_url):
            file_path = Path(__file__).parent.joinpath('products', f'{product["id"]}.json')
            self.save(product, file_path)


    def save(self, data: dict, file_path):
        with open(file_path, 'w', encoding='UTF-8') as file:
            json.dump(data, file, ensure_ascii=False)


    def get_response(self, url, **kwargs):
        while True:
            try:
                response = requests.get(url, **kwargs)
                if response.status_code != 200:
                    raise Exception 
                time.sleep(0.05)
                return response
            except Exception:
                time.sleep(0.25)


    def parse(self, url):
        while url:
            response = self.get_response(url, headers=self.headers)
            data = response.json()
            url = data["next"]
            for product in data['results']:
                yield product



class Parse5kaCategories(Parser5ka):
    def run(self):
        for product in self.parse(self.start_url):
            file_path = Path(__file__).parent.joinpath('products', f'{product["id"]}.json')
            self.save(product, file_path)


if __name__ == "__main__":
    parser = Parser5ka(url)
    parser.run()
