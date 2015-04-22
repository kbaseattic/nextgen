module KmerAnnotationByFigfam {

    funcdef get_dataset_names() returns (list<string> dataset_names);
    funcdef get_default_dataset_name() returns (string default_dataset_name);

    typedef structure
    {
	int kmer_size;
	string dataset_name;
	int return_scores_for_all_proteins;
	int score_threshold;
	int hit_threshold;
	int sequential_hit_threshold;
	int detailed;
	int min_hits;
	int min_size;
	int max_gap;
    } kmer_annotation_figfam_parameters;

    typedef tuple<int offset, string oligo, string prot_function, string otu> hit_detail;

    typedef tuple<string id, string prot_function, string otu, int score,
	int nonoverlapping_hits, int overlapping_hits, list<hit_detail> details> hit;

    typedef tuple<int nhits, string id, int beg, int end, string protein_function, string otu> dna_hit;

    funcdef annotate_proteins(list<tuple<string id, string protein>> proteins, kmer_annotation_figfam_parameters params)
	returns(list<hit> hits);

    funcdef annotate_proteins_fasta(string protein_fasta, kmer_annotation_figfam_parameters params)
	returns(list<hit> hits);

    funcdef call_genes_in_dna(list<tuple<string id, string dna>> dna, kmer_annotation_figfam_parameters params)
      returns(list<dna_hit> hits);

    funcdef estimate_closest_genomes(list<tuple<string id, string function, string translation>> proteins, 
    				     string dataset_name)
      returns(list<tuple<string genome_id, int score, string genome_name>> output);
};
