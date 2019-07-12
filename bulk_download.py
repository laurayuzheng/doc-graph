import urllib.request
from bs4 import BeautifulSoup

DIRECTORY = '/Users/laurazheng/Desktop/NASA Project/doc-graph/Papers/'
url = 'https://arxiv.org/search/?query=earth+&searchtype=all&abstracts=show&order=-announced_date_first&size=50&start=0'
data = urllib.request.urlopen(url).read()
soup = BeautifulSoup(data,features='lxml')

tags = soup.find_all(title='pdf')

links = []
for tag in tags:
    links.append(tag['href'])

#print(links)

for link in links:
    title = link.rsplit('/', 1)[-1] + '.pdf'
    #print(title)
    response = urllib.request.urlopen(link)
    file = open(DIRECTORY + title,'wb')
    file.write(response.read())
    file.close()

print('done downloading all files: ' + links)
