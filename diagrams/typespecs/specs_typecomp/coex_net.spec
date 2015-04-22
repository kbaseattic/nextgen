/* 
	Module Coexpression Networks version 1.0
	This module provides a typed object for Coexpression Network

*/

module CoexNetworks : Networks
{

	/* Type of edge in a network */
	typedef string dataset_source_type;
	
	/* Provides detailed information about the source of a dataset.
		string id - A unique  identifier of a dataset source
		string name - A name of a dataset source
    	    	dataset_source_ref reference - Reference to a dataset source
    	    	string description - General description of a dataset source
    	    	string resourceURL - URL of the public web resource hosting the data represented by this dataset source
		string source_type - Unique for Coex to identify the source information type whether it is from workspace, shock, or raw file
	*/	
  	typedef structure {
		string id;
    		string name;
		dataset_source_ref reference;    
		string description;
		string resource_url;
  	} DatasetSource;  
  
  
  	/* Represents a particular dataset.
		string id - A unique  identifier of a dataset 
    	    	string name - The name of a dataset
    	    	string description - Description of a dataset
    	    	network_type networkType - Type of network that can be generated from a given dataset
		dataset_source_ref sourceReference - Reference to a dataset source
		list<taxon> taxons - A list of NCBI taxonomy ids of all organisms for which genomic features (genes, proteins, etc) are used in a given dataset 
    	    	mapping<string,string> properties - Other properties  		  		
                New coex specific attributes can be dataset properties
  	*/
 	typedef structure {
	    	string id;
    		string name;
		string description;
		network_type type;
		dataset_source_ref source_ref;
		list<taxon> taxons;
		mapping<string,string> properties;
                string original_data_id; /* coex addition : workspace id / shock node id*/
                string original_data_type; /* coex addition : workspace/shock/user_uploaded/etc */
                string coex_filtering_arguments; /* coex addition */
                string coex_network_arguments; /* coex addition */
                string coex_clustering_arguments; /* coex addition */
  	} CoexDataset;
  

	/* Represents a node in a network.
	   	string id - A unique  identifier of a node 
		string name - String representation of a node. It should be a concise but informative representation that is easy for a person to read.
    	    	string entity_id - The identifier of a  entity represented by a given node 
		node_type type - The type of a node
    	    	mapping<string,string> properties - Other properties of a node
    	    	mapping<string,string> user_annotations - User annotations of a node		
	*/  
  	typedef structure {
   		string id;  
		string name;
		string entity_id;
		node_type type;
		mapping<string,string> properties;
		mapping<string,string> user_annotations;
  	} Node;
  
  	/* Represents an edge in a network.
	   	string id - A unique  identifier of an edge 
    	    	string name - String representation of an edge. It should be a concise but informative representation that is easy for a person to read.
    	    	string node_id1 - Identifier of the first node (source node, if the edge is directed) connected by a given edge 
    	    	string node_id2 - Identifier of the second node (target node, if the edge is directed) connected by a given edge
    	    	Boolean	directed - Specify whether the edge is directed or not. "true" if it is directed, "false" if it is not directed
    	    	float confidence - Value from 0 to 1 representing a probability that the interaction represented by a given edge is a true interaction
    	    	float strength - Value from 0 to 1 representing a strength of an interaction represented by a given edge
    	    	string dataset_id - The identifier of a dataset that provided an interaction represented by a given edge
		mapping<string,string> properties - Other edge properties
    	    	mapping<string,string> user_annotations - User annotations of an edge    	    		
  	*/
  	typedef structure {
	    	string id;  
    		string name;
		string node_id1;
		string node_id2;
		boolean	directed;
		float confidence;
		float strength;
		string dataset_id;
		mapping<string,string> properties;
		mapping<string,string> user_annotations;  
  	} Edge;
  

	/* Represents a network
	        string id - A unique  identifier of a network 
    	    	string name - String representation of a network. It should be a concise but informative representation that is easy for a person to read.
		list<Edge> edges - A list of all edges in a network
		list<Node> nodes - A list of all nodes in a network
		list<Dataset> datasets - A list of all datasets used to build a network
		mapping<string,string> properties - Other properties of a network
		mapping<string,string> user_annotations - User annotations of a network  
	*/  
  	typedef structure {    
		string id;
		string name;
		list<Edge> edges;
		list<Node> nodes;
		list<CoexDataset> datasets;
		mapping<string,string> properties;
		mapping<string,string> user_annotations;  
  	} CoexNetwork;
  
};
