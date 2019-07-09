package text_extractor;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;

import org.apache.commons.io.FilenameUtils;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.output.Format;
import org.jdom.output.XMLOutputter;

import pl.edu.icm.cermine.ContentExtractor;
import pl.edu.icm.cermine.exception.AnalysisException;

public class TextExtractor {
	
	// paths to read pdfs from locally and to write xml files to
	static String parentDirectory = (new File(System.getProperty("user.dir"))).getParent();
	static String writePath = parentDirectory + "/xml-files/";
	static String readPath = parentDirectory + "/Papers/";

	public static void main(String[] args) throws AnalysisException, IOException{	
		System.out.println("Working... ");
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
				if (!textExt.checkXML(writePath + title)) {
					textExt.writeXML(child.getName(), title + ".xml");
				}
			}
		}
		System.out.println("Finished!");
	}
	
	private void writeXML(String filepath, String xmlName) throws AnalysisException, IOException{
		ContentExtractor extractor = new ContentExtractor();
		InputStream inputStream = new FileInputStream(readPath + filepath);

		extractor.setPDF(inputStream);
		Element result = extractor.getContentAsNLM();
		
		Document doc = new Document();
		doc.setRootElement(result);
		
		XMLOutputter xmlOutput = new XMLOutputter();
		xmlOutput.setFormat(Format.getPrettyFormat());
		xmlOutput.output(doc, new FileWriter(writePath + xmlName));
		
		System.out.println(xmlName + " Saved!");
	}
	
	// checks whether or not the pdf has already been parsed to XML
	private boolean checkXML(String paperName) {
		boolean exists = false;
		File temp = new File(paperName, ".xml");
		exists = temp.exists();
		return exists;
	}
	
}
