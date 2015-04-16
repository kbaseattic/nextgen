# Queries our data model should support

## Top 20 queries

Try to model the requirements of the system by listing the top 20 queries

1. for this model, show me associated genomes
2. how many genomes have at least one gene that produces this protein
3. show me what connects to this model
4. what can I do with a model
5. what can I do with a matrix of values
6. ability to QA the biological accuracy of the data
  Examples : 
    A. Genomes without contigs
    B. Coding sequence that does not code for the corresponding amino acid sequence
    C. Genomes without coding sequences
    D. Wrong genetic code
    E. Features without location information
    F. Features with ordinal counts being inconsistent with location counts 
    G. Coding Sequence irregularities (way too small, too big, not starting in Methionine but ending in Methionine)
    H. Exon ordinal position is reversed
    I. Multiple location features located on both strands
7. ability to query the integrity of the data
  Examples : 
    A. Orphaned links (causing queries to fail, erroneous results, etc)
    B. duplicate relationships (causing cartesian products)
    C. Inconsistencies between top level summary and the real data. (ex. Genome says 10 contigs but really has 12, Gene says 4507bp but adding up the exons it is really 5100bp, )
    D. Data incompleteness (no source, domain, taxonomy for a genome)
8. ability find features by various aliases
9. ability to look at splice variants (cds->mRNA->locus)
