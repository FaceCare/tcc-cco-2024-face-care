from model.crawler_model import Crawler
from decorator.log_decorator import log_decorator
import requests
from bs4 import BeautifulSoup

class CrawlerImagesService(Crawler):

    def __init__(self, search: str, num_pages: int):
        super().__init__()
        self.search = search
        self.base_url = "https://www.google.com/search?q=%s&ie=utf-8&oe=utf-8"
        self.num_pages = num_pages

    @log_decorator
    def list_images_url(self):
        
        image_urls = []
        query = 'rosto acne'
        for page in range(self.num_pages):
            start_index = page * 100
            url = f"https://www.google.com/search?q={query}&tbm=isch&start={start_index}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                images = soup.find_all('img')
                
                for img in images:
                    src = img.get('src')
                    if src:
                        if 'https' in src or 'http' in src:
                            image_urls.append(src)
            else:
                print(f"Failed to retrieve data for page {page + 1}.")
                
        for i, url in enumerate(image_urls, 1):
            print(f"Image {i}: {url}")

        return image_urls
