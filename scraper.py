from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init


init(autoreset=True)

print(Fore.YELLOW + "ryzsb's Roblox Decal Scraper")


def fetch_image_urls_with_selenium(page_url):
    """Fetch image URLs using Selenium to handle dynamic content and pagination."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(page_url)

    time.sleep(5)  

    image_urls = []

    while True:
        try:
          
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            for img_tag in soup.find_all('img', {'src': True}):
                img_url = img_tag['src']
                if 'rbxcdn.com' in img_url:
                    img_url = img_url.replace("/150/150/", "/1024/1024/")
                    image_urls.append(img_url)

           
            next_button = driver.find_element(By.CSS_SELECTOR, '.pager-next button')
            if 'ng-disabled' in next_button.get_attribute('class'):
                print(Fore.GREEN + "No more pages to load.")
                break 
            else:
                next_button.click()
                time.sleep(5)

        except Exception as e:
            print(Fore.RED + f"Error fetching image URLs: {e}")
            break

    driver.quit()
    return image_urls


def download_images(image_urls, download_folder="downloads"):
    """Download images for all matching asset links."""
    os.makedirs(download_folder, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}

    for index, url in enumerate(image_urls):
        try:
      
            response = requests.get(url, headers=headers, stream=True)
            if response.status_code == 200:
                file_path = os.path.join(download_folder, f"image_{index + 1}.webp")
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(Fore.GREEN + f"Downloaded: {file_path}")
            else:
                print(Fore.YELLOW + f"Image not found at: {url}")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Failed to download image from {url}: {e}")


def main():
    print(Fore.YELLOW + "Welcome to the Roblox Decal Scraper!")
   
    page_url = input(Fore.LIGHTYELLOW_EX + "Enter the Roblox page URL: ").strip()

    print(Fore.CYAN + "\nExtracting image URLs from all pages...\n")
    image_urls = fetch_image_urls_with_selenium(page_url)

    if image_urls:
        print(Fore.GREEN + "\nExtracted Image URLs:")
        for url in image_urls:
            print(Fore.CYAN + url)

        download_choice = input(Fore.LIGHTYELLOW_EX + "\nDo you want to download the images? (yes/no): ").strip().lower()
        if download_choice in ["yes", "y"]:
            print(Fore.CYAN + "\nDownloading images...")
            download_images(image_urls)
            print(Fore.GREEN + "\nDownload complete!")
        else:
            print(Fore.RED + "\nSkipping image downloads.")
    else:
        print(Fore.RED + "No image links found or an error occurred.")


if __name__ == "__main__":
    main()
