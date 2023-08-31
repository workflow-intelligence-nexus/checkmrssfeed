import requests
from xml.etree import ElementTree as ET
import sys
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def check_url(url):
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    if not url or "://" not in url:
        print(f"Skipping invalid URL: {url}")
        return True  # or False, depending on how you want to handle this case

    try:
        response = session.head(url, allow_redirects=True, timeout=10)
        if response.headers.get('Content-Type') == 'application/xml':
            response = session.get(url, timeout=10)
            if "<Code>AccessDenied</Code>" in response.text:
                return False
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
        return False
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
    print(f"Total number of URLs with Access Denied: {len(non_downloadable_urls)}")
    for url in non_downloadable_urls:
        print(url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checkmrss.py <MRSS_Feed_URL>")
        sys.exit(1)

    feed_url = sys.argv[1]
    main(feed_url)

