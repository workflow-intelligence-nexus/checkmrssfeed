import requests
import xml.etree.ElementTree as ET
import sys
from concurrent.futures import ThreadPoolExecutor

def check_url(url, entry_id):
    if url == 'NOT_POSSIBLE_TO_GENERATE_URL_FOR_FILE':
        print(f'Key_Art file for ID {entry_id} was not found')
        return True
    try:
        response = requests.head(url, allow_redirects=True)
        if response.headers.get('Content-Type') == 'application/xml':
            response = requests.get(url)
            if '<Code>AccessDenied</Code>' in response.text:
                return False
    except Exception as e:
        print(f'Error checking URL {url}: {e}')
    return True

def check_urls(urls, entry_ids):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(check_url, urls, entry_ids))
    return results

def main(feed_url):
    response = requests.get(feed_url)
    root = ET.fromstring(response.content)
    urls_to_check = []
    entry_ids = []
    for entry in root.findall('.//item'):
        entry_id = entry.find('id').text if entry.find('id') is not None else 'Unknown'
        urls = [elem.attrib['url'] for elem in entry.findall('.//media:thumbnail', namespaces={'media': 'http://search.yahoo.com/mrss/'})]
        urls_to_check.extend(urls)
        entry_ids.extend([entry_id] * len(urls))
    results = check_urls(urls_to_check, entry_ids)
    non_downloadable_urls = [url for url, result in zip(urls_to_check, results) if not result]
    print('URLs with Access Denied:')
    for url in non_downloadable_urls:
        print(url)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python checkmrss.py <MRSS_Feed_URL>')
        sys.exit(1)
    feed_url = sys.argv[1]
    main(feed_url)
