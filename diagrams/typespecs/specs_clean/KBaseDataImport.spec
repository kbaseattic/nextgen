module KBaseDataImport {

	/* Returns the current running version of the NarrativeMethodStore. */
	 funcdef ver() returns (string);

	/* List of names of genomes that can be used for 'import_ncbi_genome' method */
	funcdef get_ncbi_genome_names() returns (list<string>);

	typedef structure {
		string genome_name;
		string out_genome_ws;
		string out_genome_id;
	} import_ncbi_genome_params;

	/* Import genome from NCBI FTP 'ftp://ftp.ncbi.nih.gov/genomes/Bacteria/' into worspace object */ 
	funcdef import_ncbi_genome(import_ncbi_genome_params input) returns () authentication required;
	
	funcdef upload(string input, string output, string workspace, string object_name, mapping<string, string> props) returns (tuple<string, string> job_ids) authentication required;
};