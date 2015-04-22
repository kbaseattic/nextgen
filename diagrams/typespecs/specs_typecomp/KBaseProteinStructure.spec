/* Module KBaseProteinStructure v0.1
   This service provides PDB structure ids which correspond to 
   KBase protein sequences.  In cases where there is exact match
   to a PDB sequence, close matches (via BLASTP) are reported.

   There are two methods or function calls:
     lookup_pdb_by_md5 - accepts one or more MD5 protein identifiers
     lookup_pdb_by_fid - accepts one or more feature ids (or CDS id)
   Both return a table of matches which include PDB id, 1 or 0 for
   exact match, percent identity and alignment length.    
*/

module KBaseProteinStructure { 


    /* KBase protein MD5 id  */
    typedef string md5_id_t;

    /* list of protein MD5s */
    typedef list<md5_id_t> md5_ids_t;

    /* KBase feature id, ala "kb|g.0.peg.781" */
    typedef string feature_id_t;

    /* list of feature ids */
    typedef list<feature_id_t> feature_ids_t;

    /* PDB id */	
    typedef string  pdb_id_t;

    /* subchains of a match, i.e. "(A,C,D)" */
    typedef string  chains_t;

    /* 1 (true) if exact match to pdb sequence */
    typedef int     exact_t;
    
    /* % identity from BLASTP matches */
    typedef float   percent_id_t; 

    /* BLASTP alignment length  */ 
    typedef int     align_length_t;

    /* returned data from match */
    typedef structure {
                       pdb_id_t        pdb_id;
                       chains_t        chains;
                       exact_t         exact;
                       percent_id_t    percent_id;
                       align_length_t  align_length;
                      } PDBMatch;

    /* list of match records */
    typedef list<PDBMatch> PDBMatches;

    typedef mapping<md5_id_t,PDBMatches> md5_to_pdb_matches;

    typedef mapping<feature_id_t,PDBMatches> fid_to_pdb_matches;
 
    /*FUNCTIONS*/
    
    /* primary function - accepts a list of protein MD5s.  returns a hash (mapping?)  */
    /* of each to a list of PDBMatch records */
    funcdef lookup_pdb_by_md5( md5_ids_t input_ids ) returns( md5_to_pdb_matches results);

    /* primary function - accepts a list of protein MD5s.  returns a hash (mapping?)  */
    /* of each to a list of PDBMatch records */
    funcdef lookup_pdb_by_fid( feature_ids_t feature_ids ) returns( fid_to_pdb_matches results );
}; 
