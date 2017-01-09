Hey Rick, 

As we spoke about we need to identify someone to work on the ID mapper (or translation service or whatever) who's job it is to map genomes, genes, proteins KBase IDS to external IDs and vice versa. Any thoughts?

There is likely a strong connection to the m5nr service and Andreas and Pavel have been talking about it. But noone seems to have the cycles to get this done. Yet it is critical to a lot of functionality...

Pavel and team think the basic module spec is:


module IdMapper {

/*
	Useful refs: http://www.uniprot.org/mapping/

	IdMapper service should enable mapping of external ids to kbase ids for genomes, genes, proteins, etc.

*/



/*
	A mapping of external identifier of an object to a corresponding kbase identifier

	string source_db - source database/resource of the object to be mapped to kbase id
	string source_id - identifier of the object to be mapped to kbase id
	string kbase_id - identifier of the same object in the KBase name space
*/
typedef structure{
	string source_db;
	string source_id;
	string kbase_id;
} IdPair;


/*
	Makes an attempt to map external identifier of a genome to the corresponding kbase identifier. Multiple candidates can be found, thus a list of IdPairs is returned

string genome_id - a genome identifier. The genome identifier can be taxonomy id, genome name, or any other genome identifier
	
*/
funcdef lookup_genome(string genome_id) returns (list<IdPair>);


/*
	Makes an attempt to map external identifiers of features (genes, proteins, etc) to the corresponding kbase identifiers. Multiple candidates can be found per each external feature identifier.

	string genome_kbase_id - kbase id of a target genome
	list<string> feature_ids - list of feature identifiers. e.g. locus tag, gene name, MO locus id, etc. 
	string feature_type - type of a kbase feature to map to, e.g. CDS, pep, etc (see https://trac.kbase.us/projects/kbase/wiki/IDRegistry). If not provided, all mappings should be returned
	string source_db - the name of a database to consider as a source of a feature_ids. If not provided, all databases should be considered,

	
*/
funcdef lookup_features(string genome_kbase_id, list<string> feature_ids, string feature_type, string source_db) returns ( mapping<string, list<IdPair>> );



/*
	Returns a list of mappings of all possible types of feature synonyms and external ids to feature kbase ids for a particular kbase genome, and a given type of a feature.

	string genome_kbase_id - kbase id of a target genome
string feature_type - type of a kbase feature, e.g. CDS, pep, etc (see https://trac.kbase.us/projects/kbase/wiki/IDRegistry). If not provided, all mappings should be returned

*/
funcdef lookup_feature_synonyms(string genome_kbase_id, string feature_type) returns (list<IdPair>);



}

-- 
Adam Paul Arkin
Dean A. Richard Newton Memorial Chair
-------------------------------------
Director, Physical Biosciences Division
E.O. Lawrence Berkeley National Laboratory

Professor, Department of Bioengineering
University of California
Berkeley, CA, 94720

CEO/CSO, DOE Systems Biology Knowledgebase, http://kbase.us 
Director, Berkeley Synthetic Biology Institute, http://synbio.berkeley.edu
PI and Co-Director, ENIGMA SFA, http://enigma.lbl.gov
Investigator, Energy Biosciences Institute, http://energybiosciencesinstitute.org

Office: 512C Energy Biosciences Building (Berkeley Campus)
Mailing address:
E.O. Lawrence Berkeley National Laboratory
1 Cyclotron Road, MS 955-512L
Berkeley, CA 94720

Contact:
W: http://genomics.lbl.gov
V: 510-495-2366
C: 510-206-1389
F: 510-486-6219

Assistant:
Gwyneth A. Terry
V: 510-495-2116
E: GATerry@lbl.gov
-------------------------------------

