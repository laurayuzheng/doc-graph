from bs4 import BeautifulSoup
import glob, os
from pathlib import Path

'''
    Extracts the title and the abstract from the XML file.
'''

def extract(filename):
    ''' Description:
        - extracts the abstract based on the <abstract> or <p> tags.

        Parameters:
        - filename --> (string) path of a single file

        Returns:
        - nothing, method writes to .txt files
    '''

    cont = True

    file = open(filename, 'r')
    contents = file.read()
    soup = BeautifulSoup(contents,'xml')

    # extracts title
    titles = soup.find_all('article-title')

    # extracts abstract
    abstracts = soup.find_all('abstract')

    # extracts first paragraph in body
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
        #print(paragraphs)
        # tries to find first non empty paragraph tag
        for p in paragraphs:
            if not p.get_text().isspace():
                abstract = p.get_text()
                break
        if abstract.isspace():
            print('body was not successful, there is no abstract stored')
            cont = False

    # will not write if no abstract found
    if cont:
        file_no_extension = os.path.basename(filename) # base name, no path
        file_no_extension = os.path.splitext(file_no_extension)[0] # no ext.
        file = open(write_path + file_no_extension + '.txt','w')

        file.write(title)
        file.write('\n')
        file.write(abstract)

if __name__ == "__main__":

    dir_path = os.path.dirname(os.path.realpath(__file__))
    read_path = dir_path + '/xml-files/*.xml'
    write_path = dir_path + '/extracted_text/'
    files = glob.glob(read_path)

    # extracts from list of string paths
    for filename in files:
        xml_file = Path(os.path.splitext(filename)[0] + '.txt')
        if not xml_file.exists():
            extract(filename)
