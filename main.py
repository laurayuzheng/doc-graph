''' The main file that executes modules for application. Represents the whole process
Each part can be controlled by the part list below-- certain parts can be switched off.
'''

import create_json
import extract_abstract
import bulk_download
import formatJSON

import glob, json, os
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from pathlib import Path
from py4j.java_gateway import JavaGateway
from pathlib import Path

# like a switch to control which parts are executed
part = [0,0,0,0,1]

parent_directory = os.path.dirname(os.path.realpath(__file__))
text_path = parent_directory + '/extracted_text/'
xml_path_read = parent_directory + '/xml-files/cermine/*.xml'
xml_path_write = parent_directory + '/xml-files/cermine/'
xml_path_read2 = parent_directory + '/xml-files/arXiv/*.xml'
xml_path_write2 = parent_directory + '/xml-files/arXiv/'
txt_path_read = parent_directory + '/extracted_text/*.txt'
txt_path_write = parent_directory + '/extracted_text/'

pdf_path = parent_directory + '/Papers/'

data_filename = 'data.json'

# downloads from arXiv queries
if (part[0]):
    bulk_download.download_abstracts()

# uses py4j local server to run Java in this python script
# Java server must be running when this is executed
if (part[1]):
    print('Executing Cermine metadata parser from pdfs... ')
    gateway = JavaGateway()
    random = gateway.jvm.java.util.Random()
    java_app = gateway.entry_point
    java_app.writeAll(xml_path_write, pdf_path)

# extracts from list of string paths using extract_abstract module
if (part[2]):
    print('Extracting abstracts to xml files using sci-kit learn module... ')
    files = glob.glob(xml_path_read)
    for filename in files:
        txt_file = Path(os.path.splitext(filename)[0] + '.txt')
        if not txt_file.exists():
            extract_abstract.extract(filename, txt_path_write)

    files = glob.glob(xml_path_read2)
    for filename in files:
        print(filename)

        #txt_file = Path(os.path.splitext(filename)[0] + '.txt')
        #if not txt_file.exists():
        extract_abstract.extract_arXiv(filename, txt_path_write)

# creating JSON file using create_json module
if (part[3]):
    print('Calculating similarities and creating JSON files... ')
    text_files = glob.glob(txt_path_read)
    similarities = create_json.get_similarities(text_files)
    method_similarities = create_json.get_method_similarities(text_files)
    #print(method_similarities)
    #print(text_files[1])
    create_json.create_json(similarities.A, method_similarities, text_files, data_filename)

# formats data.json to copy and paste into HTML file
if (part[4]):
    formatJSON.format(data_filename)

print('Finished!')
