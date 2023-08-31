import requests
from xml.etree import ElementTree as ET
import sys
from concurrent.futures import ThreadPoolExecutor

def check_url(url):
    if not url or "://" not in url:
        print(f"Skipping invalid URL: {url}")
        return True  # or False, depending on how you want to handle this case

    try:
        response = requests.head(url, allow_redirects=True)
        if response.headers.get('Content-Type') == 'application/xml':
            response = requests.get(url)
            if "<Code>AccessDenied</Code>" in response.text:
                return False
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
    return True

def check_urls(urls):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(check_url, urls))
    return results

def main(feed_url):
    response = requests.get(feed_url)
    root = ET.fromstring(response.content)

    urls_to_check = [element.get('url') for element in root.findall(".//*[@url]")]
    results = check_urls(urls_to_check)
    non_downloadable_urls = [url for url, result in zip(urls_to_check, results) if not result]

    print("URLs with Access Denied:")
    for url in non_downloadable_urls:
        print(url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checkmrss.py <MRSS_Feed_URL>")
        sys.exit(1)

    feed_url = sys.argv[1]
    main(feed_url)
