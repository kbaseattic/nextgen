# Create new instance of Neo4jGraph graph (provide a location of neo4j)  
  
gremlin> g = new Neo4jGraph('/Applications/neo4j-community-2.2.1/')                                             
==>neo4jgraph[EmbeddedGraphDatabase [/Applications/neo4j-community-2.2.1]]  
  
# Load graphml file  
  
gremlin> g.loadGraphML('/kb/dev_container/modules/nextgen/diagrams/typespecs/graphs_tinker/_combined.graphml')  
==>null  
  
# Check the number of nodes in the graph  
  
gremlin> g.V.count()  
==>1665  
  
# Look at the content of few nodes  
  
gremlin> g.V[0..5].map  
==>{typeName=feature_quality_measure, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.feature_quality_measure, nodeType=D}  
==>{typeName=cmonkey_motif_id, moduleName=Cmonkey, name=D.Cmonkey.cmonkey_motif_id, nodeType=D}  
==>{typeName=association_test, moduleName=Ontology, name=M.Ontology.association_test, nodeType=M}  
==>{typeName=html_file, moduleName=Tree, name=D.Tree.html_file, nodeType=D}  
==>{typeName=ws_genome_id, moduleName=GenomeComparison, name=D.GenomeComparison.ws_genome_id, nodeType=D}  
==>{typeName=run_pipeline, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.run_pipeline, nodeType=M}  
  
# Check the number of edges in the graph  
gremlin> g.E.count()  
==>1973  
  
# Loaded modules and the number of nodes in each module  
  
gremlin> g.V.moduleName.groupCount.cap  
==>{KBasePhenotypes=18, Workspace=125, Cmonkey=16, UpstartIntegration=1, KBaseSequences=2, Empty=3, UserAndJobState=49, Ontology=39, PROM=30, CompressionBasedDistance=2, MEME=29, MOTranslation=23, KBaseFile=12, IdMap=6, KBasePPI=17, KBaseDataImport=5, TaxonomyTranslation=11, AbstractHandle=18, ProbabilisticAnnotation=29, KBaseFBA=111, AuthIntegration=3, CoExpression=4, KBaseGeneFamilies=21, KBaseCommon=6, Communities=40, GenomeAnnotation=108, KBaseAssembly=8, KBaseBiochem=49, KBaseOntology=23, KBaseCommunities=21, KBaseExpression=136, KBaseRegulation=30, ProteinInfo=23, AskKB=10, ServiceRegistry=9, RDPTools=13, ERDB_Service=12, KmerEval=23, ExpressionServices=119, Transform=9, KmerAnnotationByFigfam=10, Tree=41, AssemblyInputHandle=5, KBaseSearch=44, KBaseNarrative=4, Sim=3, KBaseProteinStructure=15, KBaseGwasData=46, GWAS=11, MAK=20, KBaseNetworks=24, GenomeComparison=7, KBaseGenomes=57, InvocationService=20, HandleMngr=3, KBaseTrees=80, AMETHSTService=4, Inferelator=9, IDServerAPI=9, NarrativeJobService=18, UserProfile=14, BAMBI=8}  
  
# Loaded modules sorted by the number of nodes  
  
gremlin> modulesStat = [:]                                                                                      
gremlin> g.V.moduleName.groupCount(modulesStat).cap  
==>{GenomeAnnotation=108, Cmonkey=16, Ontology=39, Tree=41, GenomeComparison=7, Communities=40, Workspace=125, KBaseGwasData=46, KBaseExpression=136, RDPTools=13, TaxonomyTranslation=11, InvocationService=20, KBaseTrees=80, KmerEval=23, KBaseNetworks=24, KBaseFBA=111, ExpressionServices=119, KBaseGenomes=57, KBaseSearch=44, KmerAnnotationByFigfam=10, BAMBI=8, ERDB_Service=12, MEME=29, KBaseBiochem=49, KBaseOntology=23, Inferelator=9, UserAndJobState=49, AbstractHandle=18, KBaseRegulation=30, KBaseFile=12, PROM=30, ProbabilisticAnnotation=29, AskKB=10, UserProfile=14, NarrativeJobService=18, AuthIntegration=3, KBaseCommunities=21, KBasePPI=17, CoExpression=4, KBaseGeneFamilies=21, MOTranslation=23, IDServerAPI=9, IdMap=6, ProteinInfo=23, ServiceRegistry=9, KBasePhenotypes=18, Empty=3, GWAS=11, MAK=20, KBaseAssembly=8, KBaseCommon=6, KBaseDataImport=5, UpstartIntegration=1, KBaseNarrative=4, AssemblyInputHandle=5, KBaseProteinStructure=15, HandleMngr=3, Sim=3, Transform=9, AMETHSTService=4, KBaseSequences=2, CompressionBasedDistance=2}  
gremlin> modulesStat.sort{-it.value}  
==>KBaseExpression=136  
==>Workspace=125  
==>ExpressionServices=119  
==>KBaseFBA=111  
==>GenomeAnnotation=108  
==>KBaseTrees=80  
==>KBaseGenomes=57  
==>KBaseBiochem=49  
==>UserAndJobState=49  
==>KBaseGwasData=46  
==>KBaseSearch=44  
==>Tree=41  
==>Communities=40  
==>Ontology=39  
==>KBaseRegulation=30  
==>PROM=30  
==>MEME=29  
==>ProbabilisticAnnotation=29  
==>KBaseNetworks=24  
==>KmerEval=23  
==>KBaseOntology=23  
==>MOTranslation=23  
==>ProteinInfo=23  
==>KBaseCommunities=21  
==>KBaseGeneFamilies=21  
==>InvocationService=20  
==>MAK=20  
==>AbstractHandle=18  
==>NarrativeJobService=18  
==>KBasePhenotypes=18  
==>KBasePPI=17  
==>Cmonkey=16  
==>KBaseProteinStructure=15  
==>UserProfile=14  
==>RDPTools=13  
==>ERDB_Service=12  
==>KBaseFile=12  
==>TaxonomyTranslation=11  
==>GWAS=11  
==>KmerAnnotationByFigfam=10  
==>AskKB=10  
==>Inferelator=9  
==>IDServerAPI=9  
==>ServiceRegistry=9  
==>Transform=9  
==>BAMBI=8  
==>KBaseAssembly=8  
==>GenomeComparison=7  
==>IdMap=6  
==>KBaseCommon=6  
==>KBaseDataImport=5  
==>AssemblyInputHandle=5  
==>CoExpression=4  
==>KBaseNarrative=4  
==>AMETHSTService=4  
==>AuthIntegration=3  
==>Empty=3  
==>HandleMngr=3  
==>Sim=3  
==>KBaseSequences=2  
==>CompressionBasedDistance=2  
==>UpstartIntegration=1  
  
  
# Frist 10  nodes from the GenomeAnnotation module  
  
gremlin> g.V('moduleName','GenomeAnnotation')[0..<10].map  
==>{typeName=feature_quality_measure, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.feature_quality_measure, nodeType=D}  
==>{typeName=run_pipeline, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.run_pipeline, nodeType=M}  
==>{typeName=pipeline_batch_enumerate_batches, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.pipeline_batch_enumerate_batches, nodeType=M}  
==>{typeName=reconstructionTO, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.reconstructionTO, nodeType=D}  
==>{typeName=create_genome, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.create_genome, nodeType=M}  
==>{typeName=workflow, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.workflow, nodeType=D}  
==>{typeName=annotate_proteins_similarity, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.annotate_proteins_similarity, nodeType=M}  
==>{typeName=annotation, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.annotation, nodeType=D}  
==>{typeName=estimate_crude_phylogenetic_position_kmer, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.estimate_crude_phylogenetic_position_kmer, nodeType=M}  
==>{typeName=query_classifier_taxonomies, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.query_classifier_taxonomies, nodeType=M}  
  
  
# All methods (names) from the GenomeAnnotation module  
  
gremlin> g.V('moduleName','GenomeAnnotation').has('nodeType','M').typeName     
==>run_pipeline  
==>pipeline_batch_enumerate_batches  
==>create_genome  
==>annotate_proteins_similarity  
==>estimate_crude_phylogenetic_position_kmer  
==>query_classifier_taxonomies  
==>complete_workflow_template  
==>call_pyrrolysoproteins  
==>query_classifier_groups  
==>find_close_neighbors  
==>call_features_pyrrolysoprotein  
==>call_features_rRNA_SEED  
==>enumerate_special_protein_databases  
==>set_metadata  
==>update_functions  
==>genome_ids_to_genomes  
==>genomeTO_to_reconstructionTO  
==>call_RNAs  
==>annotate_genome  
==>reconstructionTO_to_roles  
==>reconstructionTO_to_subsystems  
==>call_features_crispr  
==>enumerate_classifiers  
==>call_features_selenoprotein  
==>default_workflow  
==>classify_into_bins  
==>annotate_proteins  
==>call_features_CDS_prodigal  
==>create_genome_from_SEED  
==>call_features_prophage_phispy  
==>add_features  
==>call_selenoproteins  
==>renumber_features  
==>call_features_repeat_region_SEED  
==>call_features_strep_pneumo_repeat  
==>add_contigs  
==>call_features_CDS_genemark  
==>classify_full  
==>compute_cdd  
==>assign_functions_to_CDSs  
==>resolve_overlapping_features  
==>compute_special_proteins  
==>pipeline_batch_status  
==>pipeline_batch_start  
==>call_features_CDS_SEED_projection  
==>genomeTO_to_feature_data  
==>call_features_CDS_FragGeneScan  
==>export_genome  
==>call_features_insertion_sequences  
==>call_features_ProtoCDS_kmer_v1  
==>call_features_ProtoCDS_kmer_v2  
==>add_contigs_from_handle  
==>call_features_tRNA_trnascan  
==>annotate_proteins_kmer_v1  
==>annotate_proteins_kmer_v2  
==>call_features_strep_suis_repeat  
==>call_features_CDS_glimmer3  
==>call_features_scan_for_matches  
==>create_genome_from_RAST  
  
  
# All datatype from the GenomeAnnotation module  
  
  
gremlin> g.V('moduleName','GenomeAnnotation').has('nodeType','D').typeName  
==>feature_quality_measure  
==>reconstructionTO  
==>workflow  
==>annotation  
==>bool  
==>pipeline_batch_status  
==>pipeline_stage  
==>kmer_v2_parameters  
==>contig  
==>location  
==>contig_id  
==>fid_function_pair  
==>feature_type  
==>fid  
==>close_genome  
==>variant_of_subsystem  
==>fid_function_pairs  
==>resolve_overlapping_features_parameters  
==>fid_role_pairs  
==>kmer_v1_parameters  
==>feature_id  
==>glimmer3_parameters  
==>function  
==>compact_feature  
==>genome_quality_measure  
==>genome_id  
==>pipeline_batch_input  
==>fid_role_pair  
==>region_of_dna  
==>fid_data_tuple  
==>rna_type  
==>cdd_hit  
==>genome_metadata  
==>pipeline_batch_status_entry  
==>Handle  
==>variant_subsystem_pairs  
==>fid_data_tuples  
==>analysis_event  
==>subsystem  
==>md5s  
==>genomeTO  
==>special_protein_hit  
==>similarity_parameters  
==>feature  
==>variant  
==>md5  
==>analysis_event_id  
==>role  
==>repeat_region_SEED_parameters  
  
  
# Types and number of edges in the GenomeAnnotation module  
  
gremlin> g.E('moduleName','GenomeAnnotation').label.groupCount.cap                     
==>{METHOD_PARAM=57, METHOD_RETURN=45, SUBTYPE=30, LIST_OF=13}  
  
# Data types used as a parameter in methods in the GenomeAnnotation module  
  
gremlin> g.E('moduleName','GenomeAnnotation').has('label','METHOD_PARAM').outV.typeName.groupCount.cap  
==>{kmer_v1_parameters=2, similarity_parameters=1, glimmer3_parameters=1, genomeTO=42, reconstructionTO=2, repeat_region_SEED_parameters=1, analysis_event=1, resolve_overlapping_features_parameters=1, kmer_v2_parameters=2, workflow=2, genome_metadata=2}  
  
# Data types used as a return in methods in the GenomeAnnotation module  
  
gremlin> g.E('moduleName','GenomeAnnotation').has('label','METHOD_RETURN').inV.typeName.groupCount.cap  
==>{reconstructionTO=1, genomeTO=39, pipeline_batch_status=1, variant_subsystem_pairs=1, workflow=2, fid_data_tuples=1}  
  
# All nodes in the graph connected to the reconstructionTO datatype in the GenomeAnnotation module   
  
gremlin> g.V('moduleName','GenomeAnnotation').has('typeName', 'reconstructionTO').both.map  
==>{typeName=reconstructionTO_to_roles, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.reconstructionTO_to_roles, nodeType=M}  
==>{typeName=reconstructionTO_to_subsystems, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.reconstructionTO_to_subsystems, nodeType=M}  
==>{typeName=genomeTO_to_reconstructionTO, moduleName=GenomeAnnotation, name=M.GenomeAnnotation.genomeTO_to_reconstructionTO, nodeType=M}  
==>{typeName=fid_function_pairs, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.fid_function_pairs, nodeType=D}  
==>{typeName=fid_role_pairs, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.fid_role_pairs, nodeType=D}  
==>{typeName=variant_subsystem_pairs, moduleName=GenomeAnnotation, name=D.GenomeAnnotation.variant_subsystem_pairs, nodeType=D}  
  
# All edges in the graph connected to the reconstructionTO datatype in the GenomeAnnotation module  
  
gremlin> g.V('moduleName','GenomeAnnotation').has('typeName', 'reconstructionTO').bothE     
==>e[20][22-METHOD_PARAM->354]  
==>e[21][22-METHOD_PARAM->357]  
==>e[319][282-METHOD_RETURN->22]  
==>e[565][524-SUBTYPE->22]  
==>e[601][558-SUBTYPE->22]  
==>e[1231][1093-SUBTYPE->22]  
  
  
# All subtypes of the reconstructionTO data type in the GenomeAnnotation module  
  
gremlin> g.V('moduleName','GenomeAnnotation').has('typeName', 'reconstructionTO').in.has('nodeType','D').typeName  
==>fid_function_pairs  
==>fid_role_pairs  
==>variant_subsystem_pairs  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

