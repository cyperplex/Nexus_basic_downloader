from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import os, requests

#Global Variable definitions
req = Request("http://NEXUSURL/REPOSITORY")
html_page = urlopen(req)
soup = BeautifulSoup(html_page, "xml")


def fetch_url(url, filename):
    """
    Function to download files and save to current directory, requires two options url and file name, passed by calling
    function
    """
    if not os.path.exists(filename):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
    return filename

def parse_nexus():
    """
    Function to connect to Nexus Repository on full path and obtain a curated list of items in the repo.
    Return both a full URI to the item and the basename of the item.
    Call the download function passing in full url and base name
    """
    links = []
    print("Downloading the following files from the repository:")
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    if '../' in links:
        links.remove('../')
    for uri in links:
        test = urlparse(uri)
        filename=(os.path.basename(test.path))
        print("Downloading",filename)
        fetch_url(uri,filename)

def upload_nexus(repo_url, filename, username, password):
    files = {'file': open(filename, 'rb')}
    full_url=repo_url + filename
    requests.post(full_url, files=files, auth=(username, password))