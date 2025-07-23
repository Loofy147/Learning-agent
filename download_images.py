import json
import re
import os
import requests

def download_images_from_jsonl(jsonl_file):
    if not os.path.exists('images'):
        os.makedirs('images')

    with open(jsonl_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            text = data.get('text', '')
            source_file = data.get('metadata', {}).get('source_file', '')

            # Regex to find image URLs
            image_urls = re.findall(r'img src="(.*?)"', text)

            for url in image_urls:
                if not url.startswith('http'):
                    # Assuming the images are in the same repo
                    base_url = "https://raw.githubusercontent.com/bregman-arie/devops-exercises/master/"
                    full_url = base_url + url
                else:
                    full_url = url

                try:
                    response = requests.get(full_url, stream=True)
                    response.raise_for_status()

                    # Get the filename from the URL
                    filename = os.path.join('images', os.path.basename(url))

                    with open(filename, 'wb') as img_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            img_file.write(chunk)
                    print(f"Downloaded {full_url} to {filename}")

                except requests.exceptions.RequestException as e:
                    print(f"Error downloading {full_url}: {e}")
                    with open("missing_images.txt", "a") as f:
                        f.write(f"{full_url}\n")

if __name__ == "__main__":
    download_images_from_jsonl('dataset.jsonl (3).txt')
