# Unveiling the Oral Microbiome: Genomic Insights into SGB748 and Its Role in Health and Disease
### _Computational Microbial Genomics Report_

---
## Frederick , FAC, Abi Chahine
M.Sc. in Quantitative & Computational Biology, University of Trento, Italy
## Pietro Maria, PME, Emidi
M.Sc. in Quantitative & Computational Biology, University of Trento, Italy 
## Andrea, AN, Naclerio
M.Sc. in Quantitative & Computational Biology, University of Trento, Italy

---

## Goal
Analyzing the genomic and metagenomic features of SGB748 MAGs from oral samples to uncover their role in health and peri-implant diseases through patient metadata integration.

---

## Introduction

Understanding the microbial communities in the oral cavity is essential for uncovering their role in health and disease. This study focuses on a set of 30 Metagenome-Assembled Genomes (MAGs), all classified under the same Species Genome Bin (SGB748), with the goal of gaining deeper insights into their genomic and metagenomic characteristics.  

These MAGs were reconstructed from oral samples collected from patients who had undergone dental implant procedures. To add context to the genomic data, patient metadata, including vitals, smoking habits, and health status, was incorporated. The patients were categorized as healthy or diagnosed with mucositis or peri-implantitis. Namely, peri-implantitis is a microbe-driven inflammatory condition that affects the soft tissues around dental implants and, in severe cases, can lead to bone loss. Mucositis, on the other hand, refers to a broader inflammation of the oral mucosa with various potential causes.  

The oral microbiome is a diverse and dynamic ecosystem, home to hundreds of bacterial species, some of which play a role in inflammatory conditions affecting dental implants. This study aims to determine whether the analyzed MAGs belong to pathogenic or commensal strains. By integrating genomic data with patient metadata and existing literature, we explore potential links between microbial identity and host health. Ultimately, this work contributes to a growing effort to understand how shifts in the oral microbiome may influence disease progression.

## Methods

### Quality Control
Quality control was performed using CheckM (version 1.2.3), a tool that estimates genome completeness and contamination levels based on databases of single-copy core marker genes. Completeness measures the proportion of expected marker genes present in a MAG, while contamination reflects the presence of extra copies of marker genes, which may arise from sequencing errors or closely related strains. In this study, the reference lineage included 104 marker genes and 58 marker sets, which are reference gene families specific to that lineage.

Since the taxonomic placement of the MAGs was initially unknown, the Lineage Workflow, which builds a phylogenetic tree to determine the appropriate marker set, would have been the ideal approach. However, due to its high computational cost, the taxonomy workflow was used instead, with the analysis first conducted at the Domain level using bacterial marker genes.

Based on completeness and contamination scores, the MAGs were categorized into three quality groups:  
>	Low-quality: Completeness < 50% or Contamination > 5%

>	Medium-quality: Completeness ≥ 50% and Contamination ≤ 5%

>	High-quality: Completeness ≥ 90% and Contamination ≤ 5%

Following the initial assessment, PhyloPhlAn was used to further evaluate the quality of the MAGs. Given their high quality, CheckM was re-run at the Genus level to refine the quality control and validate the results. This approach aimed to improve the accuracy of completeness and contamination estimates by considering a more specific taxonomic reference.

```
## command for domain level
$ checkm taxonomy_wf domain Bacteria mags/ checkm_output_domain_level/ -t 8  
```
```
## command for genus level
$ checkm taxonomy_wf genus Peptostreptococcus mags/ checkm_output_genus_level/ -t 8
```
