# doc-graph
doc-graph is a network visualization of publications based on their textual similarities.

#### 7-15-2019 Update
Tried a different method from this article: https://medium.com/analytics-vidhya/automated-keyword-extraction-from-articles-using-nlp-bfd864f41b34
Basically tried to extract keywords, and this particular article was interesting because it also dealt with abstracts from (machine learning!!!) papers. Here are example results and pictures I got from implementing this on my project.

This one is frequent trigrams:
![frequent trigrams](/images/frequent-trigrams.png)

This one is frequent bigrams:
![frequent bigrams](/images/frequent-bigrams.png)

This is a sample of TF-IDF word frequency scores based on context for one document:
![TD-IDF example](/images/TF-IDF-example.png)

Conclusions:
It looks like the frequent bigrams and trigrams yield better intuitive results than the TDIDF-- I think TDIDF somehow rules out machine learning methods as relevant to the context. Might focus on that more as a direction for algorithm extraction this week.

#### 7-12-2019 Update
Added more documents to consider from arXiv. arXiv came with its own parsed XML that gave a clean title name and "summary", which I'm assuming is equivalent to the abstract. Here's a preview of the updated visualization, with no changes to the configuration in VisJS.
![Visualization](/images/7-12-2019-visualization.png)

## I. Getting Started
### Overview

![Framework](/images/framework.png)

* *Note: TextExtractor.java needs to be running as main.py is executed. See next section for details.*
* to simply run the project as-is, run these files:
  * TextExtractor.java in text-extractor folder
  * main.py
* make sure to have the dependencies installed, as detailed below

### Running TextExtractor.java
* import the text-extractor folder as a Maven project in Eclipse, or whatever editor is used to run Java code
  * Eclipse (from https://stackoverflow.com/questions/2061094/importing-maven-project-into-eclipse):
    1. Open eclipse
    2. Click **File** > **Import**
    3. Type Maven in the search box under **Select an import source:**
    4. Select **Existing Maven Projects**
    5. Click **Next**
    6. Click **Browse** and select *text-extractor*
    7. Click **Next**
    8. Click **Finish**
* Run the TextExtractor.java class in src folder before running main.py

### Installing Dependencies
***Note: py4j needs to be installed for both python and Java***
#### Maven
* Cermine
  * make sure Maven is installed as a plug-in on Eclipse
    * https://stackoverflow.com/a/25993960/1971003
  * already taken care of in pom.xml file, no need to download anything
  * https://github.com/CeON/CERMINE
* py4j
  * `git clone https://github.com/bartdag/py4j`
  * navigate to py4j-java folder
  * run `mvn install`
  * already included in pom.xml file

#### Python
* py4j
  * enables Java code to be called in Python scripts
  * `pip install py4j`

#### Vis.js in Jupyter Notebook
* Vis.js ZIP download
  * https://github.com/almende/vis/archive/v4.19.1.zip
* Expand and move contents into local system, and take note of its paths
* `open ~/.jupyter/jupyter_notebook_config.py`
* add `c.NotebookApp.extra_static_paths = ["$(path-to-expanded-folder)/dist"]` to the config file
* should now be able to run viz-prototype.ipynb

## II. File Descriptions
### main.py
  * main script that parses and analyzes text and builds the json file needed for visualization
  * calls Maven project TextExtractor.java, extract_abstract.py and create_json.py

### text-extractor/src/text-extractor/TextExtractor.java
  * Java code that utilizes Cermine

### extract_abstract.py
  * uses BeautifulSoup to extract abstracts from XML files
  * if abstract tag does not exist, takes contents of the first paragraph <p> tag

### create_json.py
  * uses sci-kit learn modules to generate similarities between abstracts, which comes out to be a coefficient
  * uses similarity information to generate a JSON file that can be used to visualize relationships between publications

### viz-prototype.ipynb
  * Jupyter Notebook that visualizes the JSON file
  * still the prototype version, would like to move away from Jupyter in the future

## III. Folder Descriptions
### Papers
* contains PDF files of publications downloaded from the internet

### xml-files
* contains XML files that are parsed from PDFs

### extracted-text
* contains .txt files that contain article titles and abstracts of XML files

## IV. General Notes
* Please do not change the names of the folders if cloned, since the scripts rely on these directory names
* If these directories need to be changed, they can simply be modified in main.py
* Java code *is* a Maven project.
