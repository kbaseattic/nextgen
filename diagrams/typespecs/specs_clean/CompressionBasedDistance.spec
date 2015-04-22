/*
Compression Based Distance (CBD) service

Compression-based distance (CBD) is a simple, rapid, and accurate method to
efficiently assess differences in microbiota samples.  CBD characterizes
the similarities between microbial communities via the amount of repetition
or overlap in order to determine microbial community distance.  CBD relies on
the fact that more repetitive data is the more it can be compressed.  By
combining 16S rRNA hypervariable tag data from different samples and assessing
the relative amounts of compression, there is a proxy for the similarities
between the communities.  The amount of compression is converted to a distance
by taking compression gained by combining the datasets over the total
compressed size of the individual datasets.  The distance has a value with a
minimum of 0 meaning the communities are the same and a maximum of 1 meaning
the communities are completely different.

*/

module CompressionBasedDistance
{

	/* ************************************************************************************* */
	/* CBD FUNCTIONS */
	/* ************************************************************************************* */
	
	/* All methods are authenticated. */
	authentication required;

	/* Input parameters for build_matrix function
	
		list<string> node_ids - List of Shock node ids for input sequence files
		string format - Format of input sequence files ('fasta', 'fastq', etc.)
		string scale - Scale for distance matrix values ('std' or 'inf')
		int sequence_length - Length to trim sequence reads to (shorter reads are discarded)
		int min_reads - Minimum number of reads a sequence file must contain
		int max_reads - Maximum number of reads to use from a sequence file
		int extreme - Set to true for extreme compression (slower but hopefully better ratio)
			
	*/
	typedef structure {
		list<string> node_ids;
		string format;
		string scale;
		int sequence_length;
		int min_reads;
		int max_reads;
		int extreme;
	} BuildMatrixParams;
	
	/*
      Build a distance matrix from a set of sequence files for microbiota
      comparisons.  Compression based distance uses the relative compression
      of combined and individual datasets to quantify overlaps between
      microbial communities.  Returns the job identifier of the job submitted
      to build the distance matrix.
	*/
	funcdef build_matrix(BuildMatrixParams input) returns(string job_id);
	
};
