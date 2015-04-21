package us.kbase.nextgen.dapi;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringReader;
import java.io.StringWriter;
import java.io.Writer;
import java.util.Hashtable;
import java.util.List;
import java.util.Map;

import org.apache.commons.collections15.Transformer;
import org.apache.commons.io.FileUtils;

import us.kbase.jkidl.IncludeProvider;
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
import us.kbase.kidl.KbTypeInfo;
import us.kbase.kidl.KbTypedef;
import us.kbase.kidl.KidlParseException;
import us.kbase.kidl.KidlParser;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.databind.JsonMappingException;

import edu.uci.ics.jung.graph.Graph;
import edu.uci.ics.jung.graph.SparseMultigraph;
import edu.uci.ics.jung.graph.util.EdgeType;
import edu.uci.ics.jung.io.GraphMLWriter;
import edu.uci.ics.jung.io.PajekNetWriter;

/**
 * Class to generate type-type and type-method graph for a given specfile or collection of specfiles 
 * @version 1.0
 * @author Pavel Novichkov
 *
 */
public class TypeMethodGraphGenerator {

	/**
	 * Map to store registered nodes 
	 */
	private Map<String,Node> name2node = new Hashtable<String,Node>();
	
	
	/**
	 * Represents a node in a graph
	 */
	static class Node{
		static String TYPE_DATA = "D";
		static String TYPE_METHOD = "F";

		String name;
		String type;
	
		KbTypedef typedef;
		KbFuncdef func;
		
		public Node(KbTypedef typedef){
			this.typedef = typedef;
			name = typedef.getName();
			type = TYPE_DATA;
		}		
		
		public Node(KbFuncdef func){
			this.func = func;
			name = func.getName();
			type = TYPE_METHOD;
		}			
		public String getName(){
			return name;
		}
		
		public String getType(){
			return type;
		}
		public String toString(){
			return type + "." + name;
		}
	};
	
	/**
	 * Represents an edge in a graph
	 */
	static class Edge{
		public static Edge METHOD_PARAM(){ return new Edge("METHOD_PARAM");}
		public static Edge METHOD_RETURN(){ return new Edge("METHOD_RETURN");}
		public static Edge SUBTYPE(){ return new Edge("SUBTYPE");}
		public static Edge LIST_OF(){ return new Edge("LIST_OF");}
		public static Edge HASH_KEY(){ return new Edge("HASH_KEY");}
		public static Edge HASH_VALUE(){ return new Edge("HASH_VALUE");}
		
		private String name;
		private Edge(String name){
			this.name = name;
		}
		public String getName(){
			return name;
		}	
	}
		

	/**
	 * Run TypeMethodGraphGenerator 
	 * @throws Exception
	 */
	private void run() throws Exception{
		String fileName = "/kb/dev_container/modules/expression/KBaseExpression.spec";
		
		Graph<Node, Edge> graph = new SparseMultigraph<Node, Edge>();		
		String specDocument = FileUtils.readFileToString(new File(fileName));
		populateGraph(graph, specDocument);
		exportGraphML(graph, new PrintWriter( System.out));
	}	
	
	
	/**
	 * Build a new node for a given typedef, or return the existing one if it was built already 
	 * @param typedef
	 * @return
	 */
	private Node buildNode(KbTypedef typedef){
		String name = typedef.getName();
		Node node = name2node.get(name);
		if(node == null){
			node = new Node(typedef);
			name2node.put(name, node);
		}
		return node;
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
	private void processTypedef(Graph<Node, Edge> graph, Node rootNode, Edge edge, KbType type) throws Exception{
		KbTypedef typedef = null;
		
		// If the type is either "typedef" or "typedef structure"
		if(type instanceof KbTypedef){
			typedef = (KbTypedef) type;
			type = typedef.getAliasType();
			
			// Check whether typedef was processed before
			boolean wasProcessed = name2node.containsKey(typedef.getName());
			
			// Create a new node for this typedef and add edge between this node and the rootNode
			Node node = buildNode(typedef);
			if(rootNode != null && node != null){
				//graph.
				graph.addEdge(edge, node, rootNode, EdgeType.DIRECTED);
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
			processTypedef(graph, rootNode, Edge.LIST_OF(), kbList.getElementType());
		} else if (type instanceof KbMapping){
			KbMapping kbMapping = (KbMapping) type;
			processTypedef(graph, rootNode, Edge.HASH_KEY(), kbMapping.getKeyType());
			processTypedef(graph, rootNode, Edge.HASH_VALUE(), kbMapping.getValueType());
		} else if (type instanceof KbStruct){
			KbStruct kbStruct = (KbStruct) type;			
			if(typedef == null){
				throw new Exception("If the type is KbStruct, then typedef should exist");
			}			
			// Try add edges for all subtypes 
			for(KbStructItem item: kbStruct.getItems()){
				processTypedef(graph, rootNode, Edge.SUBTYPE(), item.getItemType());
			}
		}
	}
	
	 /**
	  * Build a new node for a given function, or return the existing one if it was built already 
	  * @param func
	  * @return
	  */
	 private Node buildNode(KbFuncdef func){
		String name = func.getName();
		Node node = name2node.get(name);
		if(node == null){
			node = new Node(func);
		}
		return node;
	}
	
	 
	/**
	 * Populate a graph for a given spec file 
	 * @param graph
	 * @param specDocument
	 * @throws Exception
	 */
	private void populateGraph(Graph<Node, Edge> graph, String specDocument)
			throws Exception {
		StringReader r = new StringReader(specDocument);
		StaticIncludeProvider sip = new StaticIncludeProvider();

		Map<String, Map<String, String>> moduleToTypeToSchema = null;
		Map<?, ?> parseMap = KidlParser.parseSpecInt(r, moduleToTypeToSchema,sip);
		List<KbService> services = KidlParser.parseSpec(parseMap);
		for (KbService service : services) {
			for (KbModule module : service.getModules()) {
				for (KbModuleComp comp : module.getModuleComponents()) {

					if (comp instanceof KbTypedef) {
						KbTypedef typedef = (KbTypedef) comp;
						processTypedef(graph, null, null, typedef);
					} else if (comp instanceof KbFuncdef) {
						KbFuncdef func = (KbFuncdef) comp;
						Node funcNode = buildNode(func);

						for (KbParameter param : func.getParameters()) {
							KbType paramType = param.getType();
							if (paramType instanceof KbTypedef) {
								
								// try to add edges for subtypes
								processTypedef(graph, null, null, paramType);
								
								// add edge for dataype-method connection
								Node paramNode = buildNode((KbTypedef) paramType);
								graph.addEdge(Edge.METHOD_PARAM(), paramNode, funcNode, EdgeType.DIRECTED);
							}
						}
						for (KbParameter param : func.getReturnType()) {
							KbType returnType = param.getType();
							if (returnType instanceof KbTypedef) {
								
								// try to add edges for subtypes
								processTypedef(graph, null, null, returnType);

								// add edge for dataype-method connection
								Node returnNode = buildNode((KbTypedef) returnType);
								graph.addEdge(Edge.METHOD_RETURN(), funcNode, returnNode, EdgeType.DIRECTED);
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
	private void exportGraphML(Graph<Node,Edge> graph, Writer writer) throws IOException{
		
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
	 * Export graph in Pajek format
	 * @param graph
	 * @param writer
	 * @throws IOException
	 */
	private void exportPajek(Graph<Node,Edge> graph, Writer writer) throws IOException{
		PajekNetWriter<Node,Edge> graphWriter = new PajekNetWriter<Node,Edge>();
		
		graphWriter.save(graph, writer,
				new Transformer<Node,String>(){
					@Override
					public String transform(Node node) {
						return node.toString();
					}},
				new Transformer<Edge,Number>(){
					@Override
					public Number transform(Edge edge) {
						return 1;
					}}
		);		
	}
	

	
	
	/**
	 *  to try and learn basics of kidl 
	 * 
	 * @throws JsonGenerationException
	 * @throws JsonMappingException
	 * @throws KidlParseException
	 * @throws IOException
	 */
	private void _learn() throws JsonGenerationException, JsonMappingException, KidlParseException, IOException{
		Map<KbType, String> type2name = new Hashtable<KbType, String>();
		
		String specDocument = FileUtils.readFileToString(new File("/kb/dev_container/modules/expression/KBaseExpression.spec"));
		StringReader r = new StringReader(specDocument);
		IncludeProvider sip = new StaticIncludeProvider();
		/*
		List<String> includedModuleNames = null;
		for (String includedModuleName : includedModuleNames) {
		    String includedModuleSpec = "";
		    sip.addSpecFile(includedModuleName, includedModuleSpec);
		}
		*/		
		
		Map<String, Map<String, String>> moduleToTypeToSchema = null;
		Map<?,?> parseMap = KidlParser.parseSpecInt(r, moduleToTypeToSchema, sip);
		List<KbService> services = KidlParser.parseSpec(parseMap);
		for(KbService service: services){
			System.out.println("service: " + service.getName());
			for(KbModule module: service.getModules()){
				
				System.out.println("\t module: " + module.getModuleName());
				System.out.println("//----- Info {{");				
				for(KbTypeInfo typeInfo: module.getTypeInfoList()){
					System.out.println("\t typeInfo:" + typeInfo.getName()
							+ "; type: " + typeInfo.getRef());
				}				
				System.out.println("//----- Info }}");
				
				System.out.println("//----- NameToType {{");				
				for(String name: module.getNameToType().keySet()){
					KbType type = module.getNameToType().get(name);
					System.out.println("\t name:" + name
							+ "; type: " + type
							+ "; class: " + type.getClass().getName()
        					+ "; hashcode: " + Integer.toHexString(type.hashCode()));
					
//					type2name.put(type, name);
				}				
				System.out.println("//----- NameToType }}");
				
				
				
				for(KbModuleComp comp : module.getModuleComponents()){
					if(comp instanceof KbTypedef){
						KbTypedef typedef = (KbTypedef)comp;
						System.out.println("\t\t type: " + typedef.getName()
								+ "; class: " + typedef.getClass().getName()
								+ "; alias type: " + typedef.getAliasType());
						
						type2name.put(typedef, typedef.getName());
						
						
						KbType alias = typedef.getAliasType();
						if( alias instanceof KbScalar){
							KbScalar kbScalar = (KbScalar) alias;
							
							
							System.out.println("\t\t\t scalar IdReference: " + kbScalar.getIdReference()
									+ "; scalarType: " + kbScalar.getScalarType()
									+ "; specName: " + kbScalar.getSpecName()
									);
							
							
						} else if( alias instanceof KbList){
							KbList kbList = (KbList) alias;
							
							System.out.println("\t\t\t list element type: " + kbList.getElementType()
									+ "; class: " + kbList.getElementType().getClass().getName());
							
						} else if (alias instanceof KbMapping){
							KbMapping kbMapping = (KbMapping) alias;
							
							System.out.println("\t\t\t mapping key type: " + kbMapping.getKeyType()
									+ "; value type: " + kbMapping.getValueType()
									);							
						} else if (alias instanceof KbStruct){
							KbStruct kbStruct = (KbStruct) alias;
							
							System.out.println("\t\t\t struct name: " + kbStruct.getName()
									+ ", items: ");
							for(KbStructItem item: kbStruct.getItems()){
								System.out.println("\t\t\t\t item name: " + item.getName()
										+ "; class: " + item.getClass().getName()
										+ "; itemType: " + item.getItemType()
										+ "; itemType class: " + item.getItemType().getClass().getName()
										);								
							}

						}

						
					} else if(comp instanceof KbFuncdef){
				        KbFuncdef func = (KbFuncdef)comp;
				        System.out.println("\t\t function: " + func.getName());
				        for (KbParameter param : func.getParameters()){
				        	KbType paramType = param.getType();				        	
				        	System.out.println("\t\t\t Func param: " + param.getName() 
				        			+ "; type: " + paramType
				        			+ "; class: " + paramType.getClass().getName()
				        			+ "; hashcode: " + Integer.toHexString(paramType.hashCode())
				        			+ "; derived name: " + type2name.get(paramType));
				        }
				        for (KbParameter param : func. getReturnType()){
				        	KbType returnType = param.getType();
				        	System.out.println("\t\t\t Return param: " + param.getName()
				        			+ "; type: " + returnType
				        			+ "; class: " + returnType.getClass().getName()
				        			+ "; hashcode: " + Integer.toHexString(returnType.hashCode())
				        			+ "; derived name: " + type2name.get(returnType));
				        }						
					}
				}
			}			
		}
		
		System.out.println("//------------ check type2name");
		for(KbType type: type2name.keySet()){
			String name = type2name.get(type);
        	System.out.println("name: " + name
        			+ "; type: " + type
        			+ "; class: " + type.getClass().getName()
        			+ "; hashcode: " + Integer.toHexString(type.hashCode())
        			+ "; derived name: " + type2name.get(type));
		}
		
		
	}
	
	public static void main(String[] args) throws Exception {
		new TypeMethodGraphGenerator().run();
	}
}
