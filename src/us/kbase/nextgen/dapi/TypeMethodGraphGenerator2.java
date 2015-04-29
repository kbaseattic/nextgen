package us.kbase.nextgen.dapi;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.io.Writer;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.output.WriterOutputStream;

import us.kbase.jkidl.StaticIncludeProvider;
import us.kbase.kidl.KbFuncdef;
import us.kbase.kidl.KbList;
import us.kbase.kidl.KbMapping;
import us.kbase.kidl.KbModule;
import us.kbase.kidl.KbModuleComp;
import us.kbase.kidl.KbParameter;
import us.kbase.kidl.KbScalar;
import us.kbase.kidl.KbService;
import us.kbase.kidl.KbStruct;
import us.kbase.kidl.KbStructItem;
import us.kbase.kidl.KbType;
import us.kbase.kidl.KbTypedef;
import us.kbase.kidl.KidlParser;

import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.Vertex;
import com.tinkerpop.blueprints.impls.tg.TinkerGraph;
import com.tinkerpop.blueprints.util.GraphHelper;
import com.tinkerpop.blueprints.util.io.graphml.GraphMLWriter;


/**
 * Class to generate type-type and type-method graph for a given specfile or collection of specfiles.
 * This is a version of TypeMethodGraphGenerator that uses Tinker implementation of graphs, edges, nodes, and graphml writer 
 *  
 * @version 1.0
 * @author Pavel Novichkov
 *
 */
public class TypeMethodGraphGenerator2{
	
	private static final String NODE_TYPE_DATA = "D";
	private static final String NODE_TYPE_METHOD = "M";

	private static final String EDGE_TYPE_LIST_OF = "LIST_OF";
	private static final String EDGE_TYPE_HASH_KEY = "HASH_KEY";
	private static final String EDGE_TYPE_HASH_VALUE = "HASH_VALUE";
	private static final String EDGE_TYPE_SUBTYPE = "SUBTYPE";
	private static final String EDGE_TYPE_METHOD_PARAM = "METHOD_PARAM";
	private static final String EDGE_TYPE_METHOD_RETURN = "METHOD_RETURN";
	
	private static final Object PROPERTY_NAME = "name";
	private static final Object PROPERTY_MODULE_NAME = "moduleName";
	private static final Object PROPERTY_TYPE_NAME = "typeName";
	private static final Object PROPERTY_NODE_TYPE = "nodeType";

	/**
	 * Whether the type-type should be taking into account  
	 */
	private static boolean useType2TypeEdges;
	
	/**
	 * Whether the method-type  should be taking into account
	 */
	private static boolean useType2MethodEdges;
	
	/**
	 * Whether graphs for each individual specs should be built
	 */
	private static boolean flProcessIndividualFiles;

	/**
	 * Whether the combined graph for all specs should be built
	 */
	private static boolean flBuildSingleGraph;
	
		
	/**
	 * Include provider that provides specDocuments to be included in a given spec via "include" statement
	 */
	private StaticIncludeProvider sip;
	
		

	/**
	 * Run TypeMethodGraphGenerator 
	 * @param graphFileDir 
	 * @param specFileDir 
	 * @throws Exception
	 */
	private void run(File specFileDir, File graphFileDir) throws Exception{

		buildIncludeProvider(specFileDir);
		
		if(flProcessIndividualFiles){
			processIndividualFiles(specFileDir, graphFileDir);
		}
		if(flBuildSingleGraph){
			buildSingleGraph(specFileDir, graphFileDir);
		}
	}	
	
	/**
	 * Builds include provider 
	 * @param cleanFileDir
	 * @throws IOException
	 */
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
	
	/**
	 * Builds individual graphs for spec files
	 * @param specFileDir
	 * @param graphFileDir
	 */
	private void processIndividualFiles(File specFileDir, File graphFileDir){
		for(File specFile: specFileDir.listFiles()){
			if(specFile.getName().endsWith(".spec")){
				processSpecFile(specFile, graphFileDir);
			}
		}
	}
	
	/**
	 * Builds a combined graph for all spec files
	 * @param specFileDir
	 * @param graphFileDir
	 */
	private void buildSingleGraph(File specFileDir, File graphFileDir){
		Graph graph = new TinkerGraph();		

		// Build graph
		for(File specFile: specFileDir.listFiles()){
			if(!specFile.getName().endsWith(".spec")) continue;
			
			System.out.print("Doing spec file: " + specFile.getName() + "...");
			try{
				String specDocument = FileUtils.readFileToString(specFile);
				populateGraph(graph, specDocument);
				
				System.out.println(" Done!");
				
			} catch(Exception e){
				System.out.println(e.getMessage());
			}
		}
		
		// Export graph
		try{
			File graphFile = new File(graphFileDir, "_combined.graphml");
			FileWriter fw = new FileWriter(graphFile);
			exportGraphML(graph, fw);
			fw.flush();
			fw.close();
		}catch(Exception e){
			System.out.println(e.getMessage());
		}
	}

	
	
	/**
	 * Processes one spec file
	 * @param specFile
	 * @param exportDir
	 */
	private void processSpecFile(File specFile, File exportDir){
		try{
			System.out.print("Doing spec file: " + specFile.getName() + "...");
			File graphFile = new File(exportDir, specFile.getName() + ".graphml");
			
			Graph graph = new TinkerGraph();		
			String specDocument = FileUtils.readFileToString(specFile);
			populateGraph(graph, specDocument);
			
			FileWriter fw = new FileWriter(graphFile);
			exportGraphML(graph, fw);
			fw.flush();
			fw.close();
			System.out.println(" Done!");
			
		} catch(Exception e){
			System.out.println(e.getMessage());
		}
	}
	
	private Vertex buildNode(Graph graph, KbTypedef typedef){
		
		String id = nodeId(typedef);
		Vertex v = graph.getVertex(id);
		if(v == null){
			String moduleName = typedef.getModule();
			String typeName = typedef.getName();
			v = GraphHelper.addVertex(graph, id 
					, PROPERTY_NAME, id
					, PROPERTY_MODULE_NAME, moduleName
					, PROPERTY_TYPE_NAME, typeName
					, PROPERTY_NODE_TYPE, NODE_TYPE_DATA
					);
		}
		return v;
	}

	private Vertex buildNode(Graph graph, KbModule module, KbFuncdef funcdef){
		
		String id = nodeId(module, funcdef);
		Vertex v = graph.getVertex(id);
		if(v == null){
			String moduleName = module.getModuleName();
			String typeName = funcdef.getName();
			v = GraphHelper.addVertex(graph, id 
					, PROPERTY_NAME, id
					, PROPERTY_MODULE_NAME, moduleName
					, PROPERTY_TYPE_NAME, typeName
					, PROPERTY_NODE_TYPE, NODE_TYPE_METHOD
					);
		}
		return v;
	}

	
	
	
	/**
	 * 
	 * @param typedef
	 * @return
	 */
	private String nodeId(KbTypedef typedef){
		return NODE_TYPE_DATA + "." + typedef.getModule() + "." + typedef.getName();
	}
	
	private String nodeId(KbModule module, KbFuncdef funcdef){
		return NODE_TYPE_METHOD + "." + module.getModuleName() + "." + funcdef.getName();
	}

	
	/**
	 * Process a given type and all subtypes recursively, and add corresponding edges to the graph if needed    
	 * 
	 * @param graph
	 * @param rootNode
	 * @param edge
	 * @param type
	 * @throws Exception
	 */
	private void processTypedef(Graph graph, KbModule module, Vertex rootNode, String edgeType, KbType type) throws Exception{
		
		// Do not crete type-type edges if not needed 
		if(!useType2TypeEdges) return;
		
		KbTypedef typedef = null;
		
		// If the type is either "typedef" or "typedef structure"
		if(type instanceof KbTypedef){
			typedef = (KbTypedef) type;
			type = typedef.getAliasType();
			
			// Check whether typedef was processed before
			boolean wasProcessed = graph.getVertex(nodeId(typedef)) != null; 
			
			// Create a new node for this typedef and add edge between this node and the rootNode
			Vertex node = buildNode(graph, typedef);
			if(rootNode != null && node != null){
				GraphHelper.addEdge(graph, nextEdgeId(), node, rootNode, edgeType
						, "moduleName", module.getModuleName());
			}
			
			// Do not process typedef further if it was processed before
			if(wasProcessed){
				return;
			}
			
			// Now the new node is the root 
			rootNode = node;
		}
				
		
		if(type instanceof KbScalar){
			// nothing to be done
		} else if(type instanceof KbList){
			KbList kbList = (KbList) type;
			processTypedef(graph, module, rootNode, EDGE_TYPE_LIST_OF, kbList.getElementType());
		} else if (type instanceof KbMapping){
			KbMapping kbMapping = (KbMapping) type;
			processTypedef(graph, module, rootNode, EDGE_TYPE_HASH_KEY, kbMapping.getKeyType());
			processTypedef(graph, module, rootNode, EDGE_TYPE_HASH_VALUE, kbMapping.getValueType());
		} else if (type instanceof KbStruct){
			KbStruct kbStruct = (KbStruct) type;			
			if(typedef == null){
				throw new Exception("If the type is KbStruct, then typedef should exist");
			}			
			// Try add edges for all subtypes 
			for(KbStructItem item: kbStruct.getItems()){
				processTypedef(graph, module, rootNode, EDGE_TYPE_SUBTYPE, item.getItemType());
			}
		}
	}

	private void aggregateTypedefs(KbType type, List<KbTypedef> typedefs){
		if(type instanceof KbTypedef){
			typedefs.add( (KbTypedef) type);
		}		
		else if(type instanceof KbScalar){
			// nothing to be done
		} else if(type instanceof KbList){
			KbList kbList = (KbList) type;
			aggregateTypedefs(kbList.getElementType(), typedefs);			
		} else if (type instanceof KbMapping){
			KbMapping kbMapping = (KbMapping) type;
			aggregateTypedefs(kbMapping.getKeyType(), typedefs);
			aggregateTypedefs(kbMapping.getValueType(), typedefs);
		} else if (type instanceof KbStruct){
			KbStruct kbStruct = (KbStruct) type;			
			for(KbStructItem item: kbStruct.getItems()){
				aggregateTypedefs(item.getItemType(), typedefs);
			}
		}		
	}
	
	
	
	private static int _edgeId = 0;
	private Integer nextEdgeId() {
		return _edgeId++;
	}

	/**
	 * Populate a graph for a given spec file 
	 * @param graph
	 * @param specDocument
	 * @throws Exception
	 */
	private void populateGraph(Graph graph, String specDocument)
			throws Exception {
		StringReader r = new StringReader(specDocument);
		List<KbTypedef> mtTypedefs = new Vector<KbTypedef>();

		Map<String, Map<String, String>> moduleToTypeToSchema = null;
		Map<?, ?> parseMap = KidlParser.parseSpecInt(r, moduleToTypeToSchema,sip);
		List<KbService> services = KidlParser.parseSpec(parseMap);
		for (KbService service : services) {
			for (KbModule module : service.getModules()) {
				for (KbModuleComp comp : module.getModuleComponents()) {

					if (comp instanceof KbTypedef) {
						KbTypedef typedef = (KbTypedef) comp;
						processTypedef(graph, module, null, null, typedef);
					} else if (comp instanceof KbFuncdef) {
						KbFuncdef func = (KbFuncdef) comp;
						
						Vertex funcNode = buildNode(graph, module, func);

						for (KbParameter param : func.getParameters()) {
							mtTypedefs.clear();
							aggregateTypedefs(param.getType(), mtTypedefs);
							
							for(KbTypedef paramTypedef: mtTypedefs){
								
								// try to add edges for subtypes
								processTypedef(graph, module, null, null, paramTypedef);

								// Add type-method edge only if it was requested
								if(useType2MethodEdges) {
									// add edge for dataype-method connection
									Vertex paramNode = buildNode(graph, paramTypedef);
									GraphHelper.addEdge(graph, nextEdgeId(), paramNode, funcNode, EDGE_TYPE_METHOD_PARAM 
											,  PROPERTY_MODULE_NAME, module.getModuleName());
								}
							}
						}
						for (KbParameter param : func.getReturnType()) {
							mtTypedefs.clear();
							aggregateTypedefs(param.getType(), mtTypedefs);
							
							for(KbTypedef returnTypedef: mtTypedefs){
								
								// try to add edges for subtypes
								processTypedef(graph, module, null, null, returnTypedef);

								// Add type-method edge only if it was requested
								if(useType2MethodEdges) {
									// add edge for dataype-method connection
									Vertex returnNode = buildNode(graph, returnTypedef);
									GraphHelper.addEdge(graph, nextEdgeId(), funcNode, returnNode, EDGE_TYPE_METHOD_RETURN 
											,  PROPERTY_MODULE_NAME, module.getModuleName());
									
								}
							}
						}
					}
				}
			}
		}

	}	 
	

	/**
	 * Export a graph in the GraphML format
	 * @param graph
	 * @param writer
	 * @throws IOException
	 */
	private void exportGraphML(Graph graph, Writer writer) throws IOException{
		
		
		GraphMLWriter graphWirter = new GraphMLWriter(graph);
		graphWirter.outputGraph(new WriterOutputStream(writer));
		
		
		
		
		/*
		  Example of a node in yEd
	  	
	      <data key="d0">
	        <y:ShapeNode>
	          <y:Geometry x="165.0" y="178.0" width="30.0" height="30.0"/>
	          <y:Fill color="#CCCCFF" transparent="false"/>
	          <y:BorderStyle type="line" width="1.0" color="#000000"/>
	          <y:NodeLabel x="9.5" y="5.6494140625" width="11.0" height="18.701171875" visible="true" alignment="center"
	                       fontFamily="Dialog" fontSize="12" fontStyle="plain" textColor="#000000" modelName="internal"
	                       modelPosition="c" autoSizePolicy="content">1</y:NodeLabel>
	          <y:Shape type="rectangle"/>
	        </y:ShapeNode>
	      </data> 			 		
		 */			
/*		
		GraphMLWriter<Node,Edge> graphWriter = new GraphMLWriter<Node,Edge>();
		graphWriter.addVertexData("d0", null, null,
			    new Transformer<Node, String>() {
			        public String transform(Node node) {
			            return 
			            "<y:ShapeNode>"
			            + "<y:Shape type='rectangle'/>"
			            + "<y:Fill color='"
			            + (node.getType().equals(Node.TYPE_METHOD) ? "#FF5555" : "#CCCCFF")
			            +"' transparent='false'/>" 
			            +"<y:NodeLabel>"
			            + node.getName()
			            +"</y:NodeLabel>"
			            +"</y:ShapeNode>";
			       }
			    }
		);	
*/		
		
		/*
		 
		Example of an edge in yEd
		 
	    <edge id="e2" source="n1" target="n0">
	      <data key="d2">
	        <y:PolyLineEdge>
	          <y:Path sx="0.0" sy="0.0" tx="0.0" ty="0.0"/>
	          <y:LineStyle type="line" width="1.0" color="#000000"/>
	          <y:Arrows source="none" target="none"/>
	          <y:BendStyle smoothed="false"/>
	        </y:PolyLineEdge>
	      </data>
	      <data key="d3">222</data>
	    </edge>		
		*/
/*		
		graphWriter.addEdgeData("d2", null, null,
			    new Transformer<Edge, String>() {
			        public String transform(Edge node) {
			            return 
			            "<y:PolyLineEdge>"
			            + "<y:Arrows source='none' target='delta'/>"
			            +"</y:PolyLineEdge>";
			       }
			    }
		);			
		
		StringWriter tmpWriter = new StringWriter();
		graphWriter.save(graph,  tmpWriter);
		adoptForYEd(tmpWriter.toString(), writer);
*/		
	}	
	 
	/**
	 * Hack, to adopt graphML to be visualized in yEd 
	 * @param draphDoc
	 * @param writer
	 * @throws IOException 
	 */
	private void adoptForYEd(String draphDoc, Writer writer) throws IOException {
		BufferedReader br = new BufferedReader(new StringReader(draphDoc));
		BufferedWriter bw = new BufferedWriter(writer);
		
		bw.write(				
				"<?xml version='1.0' encoding='UTF-8'?>"
				+ "\n<graphml xmlns='http://graphml.graphdrawing.org/xmlns/graphml' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'"
				+ "\nxsi:schemaLocation='http://graphml.graphdrawing.org/xmlns/graphml http://www.yworks.com/xml/schema/graphml/1.0/ygraphml.xsd'"
				+ "\nxmlns:y='http://www.yworks.com/xml/graphml'>"
				+ "\n<key id='d0' for='node' yfiles.type='nodegraphics'/>"
				+ "\n<key id='d2' for='edge' yfiles.type='edgegraphics'/>"		
		);
		
		boolean startFound = false;
		for(String line = br.readLine(); line != null; line = br.readLine()){
			if(!startFound){
				startFound = line.startsWith("<graph ");
			}
			
			if(startFound){
				bw.append("\n");
				bw.append(line);
			}
		}
		bw.flush();
	}

	/**
	 * Main mehtod
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		
		flProcessIndividualFiles = false;
		flBuildSingleGraph = true;		
		useType2TypeEdges = true;
		useType2MethodEdges = true;
		
		File specFileDir  = new File("/kb/dev_container/modules/nextgen/diagrams/typespecs/specs_clean/");
		File graphFileDir = new File("/kb/dev_container/modules/nextgen/diagrams/typespecs/graphs_tinker/");
		
		new TypeMethodGraphGenerator2().run(specFileDir, graphFileDir);
	}
}
