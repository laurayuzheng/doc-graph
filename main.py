import create_json
import extract_abstract
import glob, json, os
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from pathlib import Path
from py4j.java_gateway import JavaGateway
from pathlib import Path

parent_directory = os.path.dirname(os.path.realpath(__file__))
text_path = parent_directory + '/extracted_text/'
xml_path_read = parent_directory + '/xml-files/*.xml'
xml_path_write = parent_directory + '/xml-files/'
txt_path_read = parent_directory + '/extracted_text/*.txt'
txt_path_write = parent_directory + '/extracted_text/'

pdf_path = parent_directory + '/Papers/'

# uses py4j local server to run Java in this python script
# Java server must be running when this is executed
print('Executing Cermine metadata parser from pdfs... ')
gateway = JavaGateway()
random = gateway.jvm.java.util.Random()
java_app = gateway.entry_point
java_app.writeAll(xml_path_write, pdf_path)

# extracts from list of string paths using extract_abstract module
print('Extracting abstracts to xml files using sci-kit learn module... ')
files = glob.glob(xml_path_read)
for filename in files:
    txt_file = Path(os.path.splitext(filename)[0] + '.txt')
    if not txt_file.exists():
        extract_abstract.extract(filename, txt_path_write)

# creating JSON file using create_json module
print('Calculating similarities and creating JSON files... ')
text_files = glob.glob(txt_path_read)
similarities = create_json.get_similarities(text_files)
create_json.create_json(similarities.A, text_files)

print('Finished!')