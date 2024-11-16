import os
import requests

from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_image(url, folder, filename, delay = 1, index: int = 0):
    try:
        response = requests.get(url, stream = True, timeout = 10)

        if response.status_code == 200:
            os.makedirs(folder, exist_ok = True)

            filepath = os.path.join(folder, filename)

            if os.path.isfile(filepath):
                print(filepath, "already exists, going to next")
                return

            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print(f"({index}) Image saved: {filepath}")
            sleep(delay)
        else:
            print(f"Cannot load {url}, Status: {response.status_code}")

    except Exception as e:
        print(f"Error loading in {__name__}. For {url}: {e}")

def scrape_images(base_url: str, output_folder="images", delay = 1, max_images = -1):
    try:
        response = requests.get(base_url, timeout = 10)
        soup = BeautifulSoup(response.text, 'html.parser')

        response.raise_for_status()
        images = soup.find_all('img')

        print(f"Downloading {f'{max_images}/' if max_images > -1 else ''}{len(images)}")

        unique_images = []
        seen_src = set()

        for img in images:
            src = img.get('src')
            if src and src not in seen_src:
                unique_images.append(img)
                seen_src.add(src)

        for index, img in enumerate(unique_images):

            img_url = img.get('src')

            if not img_url:
                continue

            img_url = urljoin(base_url, img_url)
            parsed_url = urlparse(img_url)
            
            filename = os.path.basename(parsed_url.path)

            if not filename:
                print(f'filename not existen for {img_url}')
                filename = f"image_{index + 1}.jpg"

            download_image(img_url, output_folder, filename, delay, index + 1)

            if index + 1 == max_images:
                print(f"Ended for max images ({max_images})")
                return

    except Exception as e:
        print(f"Error in {__name__}. For {base_url}: {e}")
