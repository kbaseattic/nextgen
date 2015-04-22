package us.kbase.nextgen.dapi;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringReader;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FileUtils;

import us.kbase.jkidl.StaticIncludeProvider;
import us.kbase.kidl.KbModule;
import us.kbase.kidl.KbService;
import us.kbase.kidl.KidlParseException;
import us.kbase.kidl.KidlParser;

/**
 * Checks the syntaxis of spec files, creates a list of non-redundant spec files, 
 * and reports errors for spec  files that have wrong format  
 * 
 * @version 1.0
 * @author Pavel Novichkov
 *
 */
public class SpecFilesTester {

	private final String specOkFileName = "_spec_ok.txt";
	private final String specErrorFileName = "_spec_error.txt";

	StaticIncludeProvider sip;
	BufferedWriter bwOk;
	BufferedWriter bwError;
	
	private void run(File[] specFileDirs, File cleanFileDir) throws IOException, KidlParseException {
		
		buildIncludeProvider(cleanFileDir);
		
		bwOk = new BufferedWriter(new FileWriter(new File(cleanFileDir, specOkFileName)));
		bwError = new BufferedWriter(new FileWriter(new File(cleanFileDir, specErrorFileName)));
		
		try{
			for(File dir: specFileDirs){
				for(File specFile: dir.listFiles()){
					if(specFile.getName().endsWith(".spec")){
						processSpecFile(specFile, cleanFileDir);
					}
				}		
			}
			
		} catch(Exception e){
		} finally{
			bwOk.close();
			bwError.close();
		}
		
	}
	
	
	private void buildIncludeProvider(File cleanFileDir) throws IOException {
		sip = new StaticIncludeProvider();
		
		for(File specFile: cleanFileDir.listFiles()){
			if(specFile.getName().endsWith(".spec")){
				String fileName = specFile.getName();
				String moduleName = fileName.substring(0,  fileName.indexOf(".") );
				String specDocument = FileUtils.readFileToString(specFile);
				sip.addSpecFile(moduleName, specDocument);
			}
		}		
	}


	private void processSpecFile(File specFile, File outputFileDir) throws IOException, KidlParseException {
		
		System.out.print(specFile.getName() + "\t");
		
		String moduleName = null;
		try{
			String specDocument = FileUtils.readFileToString(specFile);
			StringReader r = new StringReader(specDocument);			

			Map<String, Map<String, String>> moduleToTypeToSchema = null;
			Map<?, ?> parseMap = KidlParser.parseSpecInt(r, moduleToTypeToSchema,sip);
			List<KbService> services = KidlParser.parseSpec(parseMap);
			for (KbService service : services) {
				for (KbModule module : service.getModules()) {
					moduleName = module.getModuleName();
				}
			}
			System.out.println( moduleName);
			bwOk.write(specFile.getAbsolutePath() + "\t" + moduleName + "\n");
			FileUtils.write(new File(outputFileDir, moduleName + ".spec"), specDocument);

		} catch(Exception e){
			System.out.println("error");
			bwError.write("\n>" + specFile.getAbsolutePath() + "\n");
			e.printStackTrace(new PrintWriter(bwError));
		}
		
		
	}


	public static void main(String[] args) throws IOException, KidlParseException {
		//Show be run 3 times because of "include" statements		
		for(int i = 0; i < 3; i++){
			File[] specFileDirs = new File[]{ 
					new File("/kb/dev_container/modules/nextgen/diagrams/typespecs/specs_typecomp/"),
					new File("/kb/dev_container/modules/nextgen/diagrams/typespecs/specs_workspace/")
			};
			File cleanFileDir = new File("/kb/dev_container/modules/nextgen/diagrams/typespecs/specs_clean/");
			
			new SpecFilesTester().run(specFileDirs, cleanFileDir);
		}
	}

	
}
