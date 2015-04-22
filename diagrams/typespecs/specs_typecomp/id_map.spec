/*  The IdMap service client provides various lookups. These
    lookups are designed to provide mappings of external
    identifiers to kbase identifiers. 

    Not all lookups are easily represented as one-to-one
    mappings.
*/

module IdMap {

/*
   A mapping of aliases to the corresponding kbase identifier.

   string source_db  - the kbase id of the source
   string alias      - the identifier to be mapped to a feature id
   string kbase_id - the kbase id of the feature
*/

  typedef structure {
    string source_db;
    string alias;
    string kbase_id;
  } IdPair;

/*  Makes an attempt to map external identifier of a genome to
    the corresponding kbase identifier. Multiple candidates can
    be found, thus a list of IdPairs is returned.

    string s - a string that represents some sort of genome
    identifier. The type of identifier is resolved with the
    type parameter.

    string type - this provides information about the tupe
    of alias that is provided as the first parameter.

    An example of the parameters is the first parameter could
    be a string "Burkholderia" and the type could be
    scientific_name.

    A second example is the first parmater could be an integer
    and the type could be ncbi_taxonid.

    These are the two supported cases at this time. Valid types
    are NAME and NCBI_TAXID
*/

  funcdef lookup_genome(string s, string type)
    returns (list<IdPair> id_pairs);


/*
   Given a genome id, a list of aliases, a feature type and a source db
   return the set of feature ids associated with the aliases.

   lookup_features attempts to find feature ids for the aliases provided.
   The match is somewhat ambiguous  in that if an alias is provided
   that is associated with a feature of type locus, then the
   mrna and cds features encompassed in that locus will also be
   returned. Therefor it is possible to have multiple feature ids
   associated with one alias.

   Parameters for the lookup_features function are:
   string genome_id     - a kbase genome identifier
   list<string> aliases - a list of aliases
   string feature_type  - a kbase feature type
   string source_db     - a kbase source identifier

   To specify all feature types, provide an empty string as the
   value of the feature_type parameter. To specify all source databases,
   provide an empty string as the value of the source_db parameter.

  The lookup_features function returns a mapping between
  an alias and an IdPair.
*/

  funcdef lookup_features(string genome_id, list<string> aliases, string feature_type, string source_db)
    returns ( mapping<string, list<IdPair>> );


/*
    Returns a list of mappings of all possible types of feature
    synonyms and external ids to feature kbase ids for a
    particular kbase genome, and a given type of a feature.

    string genome_id - kbase id of a target genome
    string feature_type - type of a kbase feature, e.g. CDS,
    pep, etc (see https://trac.kbase.us/projects/kbase/wiki/IDRegistry).
    If not provided, all mappings should be returned.
*/


  funcdef lookup_feature_synonyms(string genome_id, string feature_type)
    returns (list<IdPair>);


/*
    Returns a mapping of locus feature id to cds feature id.
*/
  funcdef longest_cds_from_locus(list<string>)
    returns (mapping<string, string>);

/*
   Returns a mapping a mrna feature id to a cds feature id.
*/
  funcdef longest_cds_from_mrna(list<string>)
    returns (mapping<string, string>);




};

