# Queries our data model should support

Try to model the requirements of the system by listing the "top 20 queries".

Based on discussion on the Production Leads call on 4/16/2015, this is broken
into near-term and long-term lists.
This is not a closed document. Everyone is encouraged to add to this list, add details or questions, or help
organize it.

## Near-term

1. for this model, show me associated genomes
    1. For this genome show me all models, model results, phenotypes, experiments
2. how many genomes have at least one gene that produces this protein
3. show me what connects to this model
4. what can I do with a model
5. what can I do with a matrix of values
6. ability to QA the biological accuracy of the data. For example: 
    1. Genomes without contigs
    2. Coding sequence that does not code for the corresponding amino acid sequence
    3. Genomes without coding sequences
    4. Wrong genetic code
    5. Features without location information
    6. Features with ordinal counts being inconsistent with location counts 
    7. Coding Sequence irregularities (way too small, too big, not starting in Methionine but ending in Methionine)
    8. Exon ordinal position is reversed
    9. Multiple location features located on both strands
7. Ability to query the integrity of the data. For example: 
    1. Orphaned links (causing queries to fail, erroneous results, etc)
    2. duplicate relationships (causing cartesian products)
    3. Inconsistencies between top level summary and the real data. (ex. Genome says 10 contigs but really has 12, Gene says 4507bp but adding up the exons it is really 5100bp, )
    4. Data incompleteness (no source, domain, taxonomy for a genome)
8. ability find features by various aliases
9. ability to look at splice variants (cds->mRNA->locus)
10. Find all genes which match a given protein domain or family (e.g., TIGRFams, Pfams, COGs)
11. Find which protein domains/families match a given gene (like what gene_families service currently does)
10. Find me all homologs of this protein/gene
11. Find me all genes containing this sequence
12. For this taxon, find me all genomes
13. For this taxon, find me all related taxa with XX phylogenetic distance
14. For this gene, find me all reactions to which it is related
15. For this reaction, find me all genomes that encode a gene that is linked to it
16. For this reaction, find me all models in which it is present. 
17. For this biochemical, find me all reactions which use it and then all (meta)genomes that contain genes that link to these reactions.

## Long-term

## Directly from the services themselves

This section summarizes the functions in an arbitrary selection of 
the existing services. Not all details on input and output types are given,
just like riding an aquatic mammal (on porpoise).

1. [Genome annotation](https://github.com/kbase/genome_annotation/blob/master/GenomeAnnotation.spec)
    1. Given one or more Central Store genome IDs, convert them into genome objects
    2. Create a new genome object and assign metadata
    3. Create a new genome object based on data from the SEED project (input = genome-id)
    4. Create a new genome object based on a RAST genome
    5. Modify genome metadata
    6. Add a set of contigs to the genome object
    7. Add a set of features in tabular form
    8. Given a genome object populated with contig data, perform gene calling
       and functional annotation and return the annotated genome.
    9. Given a genome typed object, call selenoprotein features
    10. Given a genome typed object, call pyrrolysoprotein features
    11. Given a genome typed object, call insertion sequences
    12. Given a genome typed object, find instances of ribosomal RNAs in
        the genome (return = genome)
    13. Given a genome typed object, find instances of tRNAs in the genome
        (return = genome)
    14. Given a genome typed object, find instances of all RNAs we currently
        have support for detecting (return = genome)
        
2. [Protein info](https://github.com/kbase/protein_info_service/blob/master/ProteinInfoService.spec)
    1. Take as input a list of feature ids, and return a mapping of each fid to
       its operon, or domains, or a list of hits, or IPR assignments, or orthologous fids 
       in all genomes (possibly eukaryotic), or Enzyme Commission numbers, 
       or Gene Ontology assignments.
    2. Take as input a list of domain ids and return a mapping of each domain_id 
       to the fids which have that domain (reverse of fids -> domain), or to
       its text annotation as provided by its maintainer