''' This file downloads an XML file containing titles and abstracts of publications.
The XML file is retrieved based on a query to arXiv, indicated by keywords in the URLs below.
The keywords here are simply machine learning and keywords from Earth Science areas.
'''

import urllib.request
from bs4 import BeautifulSoup

DIRECTORY = '/Users/laurazheng/Desktop/NASA Project/doc-graph/Papers/'
WRITE_DIR = '/Users/laurazheng/Desktop/NASA Project/doc-graph/xml-files/arXiv/'
urls = [#'http://export.arxiv.org/api/query?search_query=all:earth+AND+all:science+OR+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:atmosphere+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:hydrology+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:geoscience+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:climate+OR+all:precipitation+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:geology+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:geophysics+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:ecology+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:meteorology+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:oceanography+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:satellite+AND+all:machine+AND+all:learning&start=0&max_results=100',
'http://export.arxiv.org/api/query?search_query=all:biogeography+AND+all:machine+AND+all:learning&start=0&max_results=100']
def download_abstracts():
    counter = 0
    file_name = 'arXiv_' + str(counter) + '.xml'

    for url in urls:
        data = urllib.request.urlopen(url).read()
        file = open(WRITE_DIR + file_name,'wb')
        file.write(data)
        file.close()
        #print(data)
    #    soup = BeautifulSoup(data,features='lxml')
    #
    #    tags = soup.find_all(title='pdf')
    #
    #    links = []
    #    for tag in tags:
    #        links.append(tag['href'])
    #
    #    print(links)
    # downloads pdfs
    #    for link in links:
    #        title = link.rsplit('/', 1)[-1] + '.pdf'
    #        #print(title)
    #        response = urllib.request.urlopen(link)
    #        file = open(DIRECTORY + title,'wb')
    #        file.write(response.read())
    #        file.close()

        counter += 1
        file_name = 'arXiv_' + str(counter) + '.xml'

        print('done downloading all files')
