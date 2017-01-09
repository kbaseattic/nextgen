/*
   This module provides methods for the classifying and matching
   of DNA sequences.
*/
module RDPTools {

     /*
        A structure of representing DNA sequences.
        
        string seqid
        
        This parameter is the sequence ID.  The format is an 'S'
        followed by 9 numbers.
        
        string bases
        
        This parameter represents the bases in the sequence.  Possible
        values are any combination of 'A', 'C', 'T', 'G' or their 
        lowercase equivalents.
     */
     typedef structure {
          string seqid;
          string bases;
     } Sequence;

    /* Handle type taken from the handle service spec. */
  
    typedef structure {
            string file_name;
            string id;
            string type;
            string url;
            string remote_md5;
            string remote_sha1;
    } Handle;

    /*
      calling Classifier
    */
    funcdef classifySeqs(list<Sequence> seqs, list<string> options) returns (Handle detailed_results, Handle hier_results) authentication optional;
    funcdef classify(list<string> handles, list<string> options) returns (Handle detailed_results, Handle hier_results) authentication optional;
	
    funcdef classify_submit(list<string> handles, list<string> options) returns (string jobid) authentication optional;
    funcdef classify_check(string jobid) returns (string status, Handle detailed_results, Handle hier_results) authentication optional;
	
    /*
      calling ProbeMatch with the default reference file or without reference file
    */
    funcdef probematchSeqs(string primers, list<string> options) returns (list<Handle> results) authentication optional;
    funcdef probematch(string primers, list<string> options, string ref_file) returns (Handle results) authentication optional;

    funcdef probematch_submit(string primers, list<string> options, string ref_file) returns (string jobid) authentication optional;
    funcdef probematch_check(string jobid) returns (string status, Handle results) authentication optional;

    /*
       Takes as input a list of options (namely, the k nearest neighbors
       and the minimum sab score), the file containing reference sequences,
       and the file containing query sequences.  It returns a list of k
       results per query sequence with the matching sequences.
    */
    funcdef seqmatch(string ref_file, string query_file, list<string> options) returns (Handle result_handle) authentication optional;

    funcdef seqmatch_submit(string ref_file, string query_file, list<string> options) returns (string jobid) authentication optional;
    funcdef seqmatch_check(string jobid) returns (string status, Handle result_handle) authentication optional;
};
