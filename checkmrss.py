import requests
from xml.etree import ElementTree as ET
import sys

def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        # Check if the content type is XML, indicating an error page
        if response.headers.get('Content-Type') == 'application/xml':
            # Optionally, you can make a GET request to check for the specific "Access Denied" message
            response = requests.get(url)
            if "<Code>AccessDenied</Code>" in response.text:
                return False
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
    return True


def main(feed_url):
    response = requests.get(feed_url)
    root = ET.fromstring(response.content)

    non_downloadable_urls = []

    # Iterate through all elements with a 'url' attribute in the XML
    for element in root.findall(".//*[@url]"):
        url = element.get('url')
        if not check_url(url):
            non_downloadable_urls.append(url)

    print("URLs with Access Denied:")
    for url in non_downloadable_urls:
        print(url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python checkmrss.py <MRSS_Feed_URL>")
        sys.exit(1)

    feed_url = sys.argv[1]
    main(feed_url)
