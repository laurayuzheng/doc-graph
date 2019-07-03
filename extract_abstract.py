from bs4 import BeautifulSoup
import glob, os

"""
    This script extracts the title and the abstract from the XML file.
"""

def extract(filename):
    cont = True

    file = open(filename, 'r')
    contents = file.read()
    soup = BeautifulSoup(contents,'xml')

    titles = soup.find_all('article-title')
    abstracts = soup.find_all('abstract')

    # this part is purely if the abstract is not found in abstract tag
    #body = soup.find_all('body')
    #print(body[0].get_text())
    #body_soup = BeautifulSoup(body[0].get_text(),'xml')
    paragraphs = soup.find_all('sec', { "id" : "sec-1"})

    if not titles[0].get_text().isspace():
        title = titles[0].get_text()
    else:
        print('there is no title tag!')
        cont = False

    abstract = ''
    if not abstracts[0].get_text().isspace():
        abstract = abstracts[0].get_text()
    else:
        #print('there is no abstract tag! trying the body..')
        print(paragraphs)
        # tries to find first non empty paragraph tag
        for p in paragraphs:
            if not p.get_text().isspace():
                abstract = p.get_text()
                break
        if abstract.isspace():
            print('body was not successful')
        #cont = False

    if cont:
        file_no_extension = os.path.basename(filename)
        file_no_extension = os.path.splitext(file_no_extension)[0]
        file = open(write_path + file_no_extension + '.txt','w')

        file.write(title)
        file.write('\n')
        file.write(abstract)

if __name__ == "__main__":
    read_path = '/Users/laurazheng/Desktop/NASA Project/xml-files/*.xml'
    write_path = '/Users/laurazheng/Desktop/NASA Project/extracted_text/'
    files = glob.glob(read_path)

    for filename in files:
        #print(filename)
        extract(filename)
