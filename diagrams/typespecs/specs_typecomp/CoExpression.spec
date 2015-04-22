/*
Co-Expression Service APIs 

 This module provides services for plant expression data in support of the coexpression
 network and ontology driven data needs of the plant sciences community. This version of
 the modules supports retrieval of the following information:
 1. Retrieval of GEO sample ID list for given EO (environmental ontology) and/or PO (plant ontology -plant tissues/organs of interest).
 2. Retrieval of the expression values for given GEO sample ID list.  
 3. For given expression values tables, it computes co-expression clusters or network (CLI only).

It will serve queries for tissue or condition specific co-expression network for biologically interesting genes/samples. Users can search differentially expressed genes in different tissues or in numerous experimental conditions or treatments (e.g various biotic or abiotic stresses). Currently the metadata annotation is provided for a subset of gene expression experiments from the NCBI GEO microarray experiments for Arabidopsis and Poplar. The samples of these experiments are manually annotated using plant ontology (PO) [http://www.plantontology.org/] and environment ontology (EO) [http://obo.cvs.sourceforge.net/viewvc/obo/obo/ontology/phenotype/environment/environment_ontology.obo]

*/

module CoExpression 
{
  /*You need to use KBase auth service to get the authentication*/
  authentication required;

  typedef structure {	  
    string ws_id; /*ws_id is the workspace id*/
    string inobj_id; /*inobj_id is expression series object id */
    string outobj_id; /*outobj_id is the output object id*/
    string p_value;/*p_value is the p-value of the statistical significance of differential expression*/
    string method;/*method is the method used for identification of differentially expressed genes*/
    string num_genes;/*num_gene is user for specify how many differentially expressed genes are needed*/
  } FilterGenesParams;
  
  /* Description of filter_genes: 
  filter_genes provides the function to identify differentially expressed genes given an expression series/experiment. An expression series/experiment contains a list of expression samples. A expression sample is the measurement of mRNA abundance in a biological sample. The design of expression profiling usually includes replicates. The replicates allows us to differ the non-relevent expression variation and the relevent expression variation.
  The replicate information is manully extracted by KBase developers. Only a part of samples has been assigned to a replicate group. For those samples without an assignment, the variation of its expression abundance is used directly.
  filter_genes now has two methods to identify differentially expressed genes: ANOVA and lor(from limma r package). The output of this function is a list of genes*/
  
  funcdef filter_genes(FilterGenesParams args) returns (list<string> job_id);

  typedef structure {
    string ws_id; /*ws_id is the workspace id*/
    string inobj_id; /* series object id */
    string outobj_id; /*outobj_id is the output object id*/
    string cut_off; /*cut_off is the statistical threshold to define a coexpression relationship*/
    string net_method; /*net_method is the method to construct coexpression network. Currently, two methods have been implemented: WGCNA(Weighted Gene Co-Expression Network) and simple PCC-based approach*/
    string clust_method; /*clust_method is the method to identify network clusters. Currently, two methods have been implemented:  WGCNA(Weighted Gene Co-Expression Network) and hclust(Hierarchical clustering)*/
    string num_modules; /*num_modules is used to define the number of modules need to be identified from the network*/
  } ConstCoexNetClustParams;



  /*Description of const_coex_net_clust
  const_coex_net_clust provides the function to build coexpression network and identify the functional modules among it.
  A functional module is a network cluster with enrichment of certain biological function. const_coex_net_clust first construct coexpression network. Then, it identifys the clusters among the network. Finally, it identifys the GeneOntology enrichment for the genes in each cluster.
  */
  funcdef const_coex_net_clust(ConstCoexNetClustParams args) returns (list<string> job_id);
};



