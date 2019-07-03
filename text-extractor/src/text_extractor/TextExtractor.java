package text_extractor;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStream;

import org.apache.commons.io.FilenameUtils;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.output.Format;
import org.jdom.output.XMLOutputter;

import pl.edu.icm.cermine.ContentExtractor;
import pl.edu.icm.cermine.exception.AnalysisException;

public class TextExtractor {
	
	// paths to read pdfs from locally and to write xml files to
	static String writePath = "/Users/laurazheng/Desktop/NASA Project/xml-files/";
	static String readPath = "/Users/laurazheng/Desktop/NASA Project/Papers/";

	public static void main(String[] args) throws AnalysisException, IOException{		
		TextExtractor textExt = new TextExtractor();
		
		File dir = new File(readPath);
		File[] fileList = dir.listFiles(new FilenameFilter() {
		    @Override
		    public boolean accept(File dir, String name) {
		        return name.endsWith(".pdf");
		    }
		});
		String title = "";
		
		if (fileList != null) {
			for (File child : fileList) {
				title = FilenameUtils.removeExtension(child.getName());
				textExt.writeXML(child.getName(), title + ".xml");
			}
		}
//		textExt.writeXML("2016-Application_of_Deep_Convolutional_Neural_Networks_for_Detecting_Extreme_Weather_in_Climate_Datasets.pdf","CNN-extreme-weather.xml");
	}
	
	private void writeXML(String filepath, String xmlName) throws AnalysisException, IOException{
		ContentExtractor extractor = new ContentExtractor();
		InputStream inputStream = new FileInputStream(readPath + filepath);

		extractor.setPDF(inputStream);
		Element result = extractor.getContentAsNLM();
//		System.out.println(result);
		
		Document doc = new Document();
		doc.setRootElement(result);
		
		XMLOutputter xmlOutput = new XMLOutputter();
		xmlOutput.setFormat(Format.getPrettyFormat());
		xmlOutput.output(doc, new FileWriter(writePath + xmlName));
		
		System.out.println(xmlName + " Saved!");
	}
	
}
