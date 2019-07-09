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
import py4j.GatewayServer;

public class TextExtractor {
	
	// paths to read pdfs from locally and to write xml files to
//	static String parentDirectory = (new File(System.getProperty("user.dir"))).getParent();
//	static String writePath = parentDirectory + "/xml-files/";
//	static String readPath = parentDirectory + "/Papers/";

	// enables Py4J, so that this can be controlled from Python main.py script
	public static void main(String[] args ) {
		TextExtractor app = new TextExtractor();
	    // app is now the gateway.entry_point
	    GatewayServer server = new GatewayServer(app);
	    System.out.println("Starting server...");
	    server.start();
//	    System.out.println("Server closed");
	}
	
//	public static void main(String[] args) throws AnalysisException, IOException{	
//		System.out.println("Working... ");
//		TextExtractor textExt = new TextExtractor();
//		
//		File dir = new File(readPath);
//		File[] fileList = dir.listFiles(new FilenameFilter() {
//		    @Override
//		    public boolean accept(File dir, String name) {
//		        return name.endsWith(".pdf");
//		    }
//		});
//		String title = "";
//		
//		if (fileList != null) {
//			for (File child : fileList) {
//				title = FilenameUtils.removeExtension(child.getName());
//				if (!textExt.checkXML(writePath + title)) {
//					textExt.writeXML(child.getName(), title + ".xml");
//				}
//			}
//		}
//		System.out.println("Finished!");
//	}
	
	// generates XML for the whole directory
	public void writeAll(String writePath, String readPath) throws AnalysisException, IOException {
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
					textExt.writeXML(readPath, writePath, child.getName(), title + ".xml");
				} else {
					System.out.println(title + ".xml already exists");
				}
			}
		}
		System.out.println("Finished!");
	}
	
	private void writeXML(String readPath, String writePath, String filepath, String xmlName) throws AnalysisException, IOException{
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
//		System.out.println("paperName: " + paperName);
		File temp = new File(paperName + ".xml");
//		System.out.println("file name: " + temp.getName());
		return temp.exists();
	}
	
}
