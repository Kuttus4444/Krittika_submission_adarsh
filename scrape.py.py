
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup as bs 


def getlinks(url: str):
    internal_links = set()
    external_links = set()
    try:
        request_url = requests.get(url)
        soup = bs(request_url.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
    
        for link in all_links:
            href = link['href']
            parsed_href = urlparse(href)
            if parsed_href.netloc == '':
                href = urljoin(url, href)
                if not href.endswith('.js'):
                    internal_links.add(href)
            else:
                if not (href.endswith('.js') or href.endswith('.com')):
                    external_links.add(href)
    
        all_tags = soup.find_all(src=True)
    
        for tag in all_tags:
            src = tag['src']
                # Check if link is internal
            parsed_src = urlparse(src)
            if parsed_src.netloc == '':
                src = urljoin(url, src)
                if not src.endswith('.js'):
                    internal_links.add(src)
            else:
                external_links.add(src)
    
    except Exception as e:
        print(url)
        print(str(e), "/n Error occured here")

    return internal_links, external_links
        


def crawl(url, visited=None, extlinks=None):
    if visited is None:
        visited = set()

    if extlinks is None:
        extlinks = set()



    internal_links, external_links = getlinks(url)
    new_links = internal_links - visited

    visited.update(internal_links)
    extlinks.update(external_links)
    #print(extlinks)

    for link in new_links:
        crawl(link, visited, extlinks)

    return (visited, extlinks)

url = "https://krittikaiitb.github.io"
ls = crawl(url)

print("Internal Links to be written", ls[0])
print("External files possible to be written", ls[1])

with open("file.txt", 'w') as fl:
    fl.write("Internal Links: \n")
    for i in ls[0]:
        fl.write(i + '\n')
    fl.write("External Links: \n")
    for i in ls[1]:
        fl.write(i + '\n')

print("finished!")