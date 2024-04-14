import requests
from bs4 import BeautifulSoup

def get_acne_faces_urls(query, num_pages=3):
    image_urls = []
    
    for page in range(num_pages):
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
    
    return image_urls

query = "rosto acne"
num_pages = 5  # Altere este número para o número desejado de páginas
image_urls = get_acne_faces_urls(query, num_pages)

for i, url in enumerate(image_urls, 1):
    print(f"Image {i}: {url}")
