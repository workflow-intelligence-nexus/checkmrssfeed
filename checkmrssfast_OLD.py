import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

def check_url(url):
    if not url or '://' not in url:
        print(f'Invalid URL: {url}')
        return
    try:
        response = requests.head(url, allow_redirects=True)
        if response.headers.get('Content-Type') == 'application/xml':
            response = requests.get(url)
            if '<Code>AccessDenied</Code>' in response.text:
                print(f'Access Denied: {url}')
    except Exception as e:
        print(f'Error checking URL {url}: {e}')

def main(mrss_feed_url):
    response = requests.get(mrss_feed_url)
    root = ET.fromstring(response.content)
    urls = [elem.attrib['url'] for elem in root.findall('.//media:thumbnail', namespaces={'media': 'http://search.yahoo.com/mrss/'})]

    with ThreadPoolExecutor() as executor:
        executor.map(check_url, urls)

if __name__ == '__main__':
    mrss_feed_url = 'https://s3.us-west-2.amazonaws.com/iconik-mrss-feeds/mrss-collection-63c43720-0581-11ee-9dea-dee45977c716.xml'
    main(mrss_feed_url)
