import os
import requests

from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from requests.exceptions import RequestException

def __ask__(q: str = ""):
    r = input(f"{q} no/yes?").lower()
    return 1 if r in ['yes', "y", "д", "да"] else 0

def __is_data_url__(url):
    return urlparse(url).scheme == "data"

def __validate__(base_url: str) -> str:
    if not base_url:
        raise ValueError("Base URL is empty!")

    parsed_url = urlparse(base_url)

    if not parsed_url.scheme:
        base_url = "http://" + base_url
        parsed_url = urlparse(base_url)

    if not parsed_url.netloc:
        raise ValueError(f"Invalid URL: {base_url}. Host is missing!")

    if not base_url.endswith('/'):
        base_url += '/'

    return base_url

def __log__(*args):
    print(*args)

def download_image(url, folder, filename, delay = 1, index: int = 0, logger = __log__):
    try:
        response = requests.get(url, stream = True, timeout = 10)

        if response.status_code == 200:
            os.makedirs(folder, exist_ok = True)

            filepath = os.path.join(folder, filename)

            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            logger(f"({index}) Image saved: {filepath}", 5)
            sleep(delay)
        else:
            logger(f"Cannot load {url}, Status: {response.status_code}")

    except RequestException as e:
        logger(f"Error loading in {__name__}. For {url}: {e}")

def scrape_images(base_url: str, output_folder="images", delay = 1, max_images = -1, logger = __log__):
    rewrite_files = -1
    try:
        base_url = __validate__(base_url)
        response = requests.get(base_url, timeout = 10)

        if response.status_code == 429: # if request blocked Python;
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
            response = requests.get(base_url, headers=headers, timeout=10)
        
        if response.history:
            __log__(f"URL was redirected to {response.url}")

        soup = BeautifulSoup(response.text, 'html.parser')

        response.raise_for_status()
        images = soup.find_all('img')

        logger(f"Downloading {f'{max_images}/' if max_images > -1 else ''}{len(images)}")

        unique_images = []
        seen_src = set()

        for img in images:
            src = img.get('src')

            if not src or __is_data_url__(src): # FIX - for data images
                continue

            if src and src not in seen_src:
                unique_images.append(img)
                seen_src.add(src)
        
        count = 0

        for index, img in enumerate(unique_images):
            img_url = img.get('src')

            if not img_url or not img_url.startswith(('http', '//')):
                logger(f"Skipping invalid URL: {img_url}")
                continue

            img_url = urljoin(base_url, img_url)
            parsed_url = urlparse(img_url)
            
            filename = os.path.basename(parsed_url.path)

            if not os.path.splitext(filename)[1]:
                filename += ".jpg"

            if not filename:
                logger(f'filename not existen for {img_url}')
                filename = f"image_{index + 1}.jpg"

            filepath = os.path.join(output_folder, filename)

            if rewrite_files == -1 and os.path.isfile(filepath):
                logger(filepath, "already exists")

                rewrite_files = __ask__("Rewrite files that existen ")

            if rewrite_files == 0:
                logger("skipping")
                continue

            download_image(img_url, output_folder, filename, delay, index, logger = logger)
            count += 1
            if count == max_images:
                logger(f"Ended for max images ({max_images})", 4)
                return 1

    except Exception as e:
        logger(f"Error in {__name__}. For {base_url}: {e}", 3)
        return 0
    
    return 1
