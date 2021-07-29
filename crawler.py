import requests
from urllib.parse import urlsplit
from bs4 import BeautifulSoup


def craw(url):
    """Getting all URLs in content of a given URL"""
    urls_processed.add(url)
    print('Processing ' + url)

    try:
        response = requests.get(url)
    except:
        return 0

    if response.status_code == 200:
        url_parts = urlsplit(url)
        domain = '{0.netloc}'.format(url_parts).replace('www.', '')
        base_url = '{0.scheme}://{0.netloc}'.format(url_parts)
        path = url[:url.rfind('/') + 1] if '/' in url_parts.path else url
        soup = BeautifulSoup(response.text, "lxml")

        for a in soup.find_all('a'):
            link = a.attrs["href"] if "href" in a.attrs else ''

            if link.startswith('/'):
                new_url = base_url + link
            elif link.startswith('mailto:'):
                new_url = link
                urls_external.add(new_url)
            elif '://' + domain in link or base_url in link:
                new_url = link
            elif link == '#':
                new_url = url
            elif not link.startswith('http'):
                new_url = path + link
            else:
                new_url = link
                urls_external.add(new_url)

            if new_url not in urls_to_process and new_url not in urls_processed and new_url not in urls_external:
                urls_to_process.append(new_url)


if __name__ == '__main__':
    seed = 'https://example.com/'
    urls_to_process = [seed]
    urls_processed = set()
    urls_external = set()

    while len(urls_to_process):
        url = urls_to_process.pop()
        craw(url)

    print('All URLs on site:')
    print(urls_processed.union(urls_external))