/*
   A mapping of aliases to the corresponding kbase identifier.

   string source_db  - the kbase id of the source
   string alias      - the identifier to be mapped to a feature id
   string feature_id - the kbase id of the feature
*/

typedef structure {
    string source_db;
    string alias;
    string feature_id;
} IdPair;

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

  The lookup_features function returns a mapping between
  an alias and an IdPair.
*/

funcdef lookup_features( string genome_id, list<string> aliases,
                         string feature_type, string source_db )
    returns ( mapping<string, list<IdPair>> );


