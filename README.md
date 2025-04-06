# Genomic and Phylogenetic Insights into SGB748: A MAG-Based Exploration of Oral Health and Disease
### _Computational Microbial Genomics Report_

---
## Frederick , FAC, Abi Chahine
> M.Sc. in Quantitative & Computational Biology, University of Trento, Italy
## Pietro Maria, PME, Emidi
> M.Sc. in Quantitative & Computational Biology, University of Trento, Italy 
## Andrea, AN, Naclerio
> M.Sc. in Quantitative & Computational Biology, University of Trento, Italy

---

## Goal
Analyzing the genomic and metagenomic features of SGB748 MAGs from oral samples to uncover their role in health and peri-implant diseases through patient metadata integration.

---

## Introduction

Understanding the microbial communities in the oral cavity is essential for uncovering their role in health and disease. This study focuses on a set of 30 Metagenome-Assembled Genomes (MAGs), all classified under the same Species Genome Bin (SGB748), with the goal of gaining deeper insights into their genomic and metagenomic characteristics.

These MAGs were reconstructed from oral samples collected from patients who had undergone dental implant procedures. To add context to the genomic data, patient metadata, including vitals, smoking habits, and health status, was incorporated. The patients were categorized as healthy or diagnosed with mucositis or peri-implantitis. Namely, peri-implantitis is a microbe-driven inflammatory condition that affects the soft tissues around dental implants and, in severe cases, can lead to bone loss. Mucositis, on the other hand, refers to a broader inflammation of the oral mucosa with various potential causes [8].

The oral microbiome is a diverse and dynamic ecosystem, home to hundreds of bacterial species, some of which play a role in inflammatory conditions affecting dental implants [11]. This study aims to determine whether the analyzed MAGs belong to pathogenic or commensal strains. By integrating genomic data with patient metadata and existing literature, we explore potential links between microbial identity and host health. Ultimately, this work contributes to a growing effort to understand how shifts in the oral microbiome may influence disease progression.

## Methods

### Quality Control
Quality control was performed using CheckM (version 1.2.3), a tool that estimates genome completeness and contamination levels based on databases of single-copy core marker genes [7]. Completeness measures the proportion of expected marker genes present in a MAG, while contamination reflects the presence of extra copies of marker genes, which may arise from sequencing errors or closely related strains. In this study, the reference lineage included 104 marker genes and 58 marker sets, which are reference gene families specific to that lineage.

Since the taxonomic placement of the MAGs was initially unknown, the Lineage Workflow, which builds a phylogenetic tree to determine the appropriate marker set, would have been the ideal approach. However, due to its high computational cost, the taxonomy workflow was used instead, with the analysis first conducted at the Domain level using bacterial marker genes [7].

Based on completeness and contamination scores, the MAGs were categorized into three quality groups:
>	Low-quality: Completeness < 50% or Contamination > 5%

>	Medium-quality: Completeness ≥ 50% and Contamination ≤ 5%

>	High-quality: Completeness ≥ 90% and Contamination ≤ 5%

Following the initial assessment, PhyloPhlAn was used to further evaluate the quality of the MAGs [10]. Given their high quality, CheckM was re-run at the Genus level to refine the quality control and validate the results [7]. This approach aimed to improve the accuracy of completeness and contamination estimates by considering a more specific taxonomic reference.

```
## Command for domain level
$ checkm taxonomy_wf domain Bacteria mags/ checkm_output_domain_level/ -t 8  
```
```
## Command for genus level
$ checkm taxonomy_wf genus Peptostreptococcus mags/ checkm_output_genus_level/ -t 8
```

### Taxonomic Analysis
Taxonomic analysis was performed using PhyloPhlAn (version 3.0.3) by leveraging the metagenomic workflow to reconstruct the phylogenetic profiles of the MAGs [10]. To optimize computational efficiency, each MAG was mapped to the single closest SGB available in the CMG2425 database, a tailored dataset designed to enhance computational speed and accuracy. This approach enabled a more precise taxonomic assignment while reducing processing time.

```
## Command for the metagenomic workflow of PhyloPhlAn
$ phylophlan_metagenomic -i mags/ -o phylophlan_output/ppa_m --nproc 4 -n 1 -d CMG2425 --database_folder ppa_db --verbose
```

### Genome Annotation
Genome annotation was performed using Prokka (version 1.14.6), a tool that identifies and labels genes within input genomes by integrating multiple databases and analytical tools [9]. As Prokka processes only one MAG at a time, a script was implemented to automate the annotation of all MAGs in the dataset. This approach ensured efficient and consistent genome annotation across all samples.

```
## Script to loop through MAGs and perform Prokka on each one of them
## Full script in 'run_prokka.sh'
for f in mags/*; do
    mag=$( basename $f .fna )
    mkdir prokka_output/${mag}
    prokka mags/${mag}.fna \
        --outdir prokka_output/${mag} \
        --prefix ${mag} \
        --compliant \
        --force
done
```

### Pangenome Analysis
Pangenome analysis was conducted using Roary (version 3.13.0), a computational tool designed for genome comparison and pangenome construction [6]. Annotated genomes in General Feature Format (*.gff), generated by Prokka, were processed by converting coding regions into protein sequences for comparative analysis [9]. A 95% sequence identity threshold was applied to determine whether two sequences represented the same gene. To account for the low number of genomes in the dataset, the core gene threshold was set to 90%, meaning a gene had to be present in at least 90% of strains to be classified as part of the core genome. The resulting pangenome categorized genes into core, soft-core, shell, and cloud genes, ranging from those present in all genomes to those found in only a few.

```
## Command for genome comparison and pangenome construction
$ roary prokka_output/*/*.gff -f roary_output -i 95 -cd 90 -p 4
```

### Phylogenetic Analysis
Phylogenetic analysis was conducted using Roary to construct a phylogenetic tree based on the presence and absence of core genes within the SGB [6]. To ensure an accurate alignment of core genes, Roary was rerun with additional parameters to generate a multiple sequence alignment (MSA). This step utilized PRANK, a multiple sequence alignment software, for precise core gene alignment, with additional refinement using MAFFT to enhance computational efficiency [3][4].

Following the alignment, the FastTreeMP plugin from Roary was used to build the phylogenetic tree, providing an evolutionary framework based on core gene variation across the analyzed genomes [6].

```
## Command for running Roary with the additional parameters
$ roary prokka_output/*/*.gff -f roary_output_w_aln -i 95 -cd 90 -p 4 -e -n
```
```
## Command for running the FastTreeMP plugin from Roary
$ FastTreeMP -pseudo -spr 4 -mlacc 2 -slownni -fastest -no2nd -mlnni 4 -gtr -nt -out
```

## Results & Discussion

The first step in the workflow involved quality control to retain good-quality genomes for analysis, defined as those with high completeness and low contamination [7]. Within SGB748, 50% of the samples were classified as high quality, while the remaining 50% were medium quality. As both categories met the quality criteria, all genomes were included in subsequent analyses (Figure 1.A).

Genome size, defined as the total nucleotide length of the genome, was observed to significantly influence the final quality of the MAGs, as completeness is inherently dependent on the number of marker genes identified (Figure 1.B). Among the 30 genomes analyzed, two exhibited 100% strain heterogeneity, indicating the presence of multiple closely related strains within these assemblies.

The GC content of the MAGs showed minimal variation across the dataset, with values consistently close to the average. This uniformity suggests that the genomes likely originate from a single strain or closely related bacterial populations (Figure 1.C).

![alt text](README_figues/figure_1.png)

Following the taxonomic assignment using PhyloPhlAn, the species was identified as Peptostreptococcus stomatis, an obligate anaerobe commonly found in the human oral cavity and associated with colorectal cancer, periodontal disease and other anaerobic infections [1][10]. Given this species identification, it would have been ideal to rerun CheckM at the species-level, however, the species was not found within the CheckM reference database. Instead, it was rerun using the genus-level classification (Peptostreptococcus) to compare the quality control metrics with the initial domain-level analysis (Figure 2) [7].

Notably, genome completeness exhibited variability, with an overall increase, but contamination levels also rose (Figures 2.A and 2.B). Despite these fluctuations, the overall quality classification of the samples remained consistent. Interestingly, the strain heterogeneity for some genomes increased, while the two genomes that initially had 100% strain heterogeneity showed a reduction to 30%. This suggests that these genomes likely originate from related Peptostreptococcus strains rather than from multiple distinct strains.

![alt text](README_figues/figure_2.png)

Additionally, comparing the presence and absence of marker genes between the domain-level and genus-level analyses confirmed that all genomes belong to the Peptostreptococcus genus. Moreover, the relatively lower completeness observed in medium-quality samples appears to be primarily due to missing genetic information rather than contamination or misclassification.

Following quality assessment, genome annotation was performed using Prokka, which identified an average of 1,295 coding sequences (CDSs) across all MAGs [9]. These CDSs include both known proteins, with characterized functions, and hypothetical proteins, for which no functional annotation could be assigned (Figure 3).

![alt text](README_figues/figure_3.png)

![alt text](README_figues/figure_4.png)

To investigate functional similarity across the dataset, all non-hypothetical CDS products were extracted and compared between the MAGs. A total of 1,140 distinct products were identified. Of these, 23 products were shared across 100% of the genomes, 227 were present in ≥90%, 576 in ≥80%, and 745 in ≥70% of the MAGs (Figure 4).

These findings suggest the presence of a conserved functional core among the genomes, with a gradual decline in shared gene content as the inclusion threshold becomes stricter. The relatively high number of shared non-hypothetical products across most genomes may reflect functional consistency within the species, supporting the hypothesis that the analyzed MAGs likely originate from bacteria within the same species.

Utilizing Roary, the pangenome, representing the complete set of genes present across all MAGs, was found to contain 3,369 genes, of which only 372 were classified as core genes, while the remaining 2,997 constituted the accessory genome (Figure 5) [6].

Notably, when comparing this result to the earlier analysis of the genome annotation with Prokka, it becomes apparent that approximately 66% of the identified genes encode hypothetical proteins. This indicates that only around 34% of the genome has been functionally annotated, highlighting a significant gap in current knowledge regarding the biology of this species.

![alt text](README_figues/figure_5.png)

As illustrated in Figure 5, the pangenome accumulation curve does not reach a plateau, indicating that the pangenome is open. An open pangenome reflects a high degree of genomic plasticity, suggesting that these strains frequently acquire new genes through horizontal gene transfer or mutation events [5]. This adaptability may reflect the ecological flexibility of the species and its ability to thrive in diverse or dynamic environments.

To further explore the phylogenetic relationships among the MAGs, the FastTreeMP function from Roary was used to generate two phylogenetic trees in Newick format: one including all MAGs in the SGB748 (Figure 6.A), and another considering only the high-quality MAGs (Figure 6.B) [6]. These trees presented notable differences compared to the initial tree produced by Roary’s Python visualization script (supplementary material). To enhance interpretability, the ETE3 Python module was employed to associate each genome with host metadata, particularly the health condition categories: healthy, mucositis, and peri-implantitis [2].

![alt text](README_figues/figure_6.png)

In the full dataset (Figure 6.A), the tree reveals two primary regions. The upper region displays a relatively even distribution of MAGs across all host conditions, suggesting the presence of a commensal strain of Peptostreptococcus stomatis that may be broadly distributed and not directly associated with disease. In contrast, the lower region contains two unrelated monophyletic clusters, one predominantly composed of mucositis-associated MAGs and the other of peri-implantitis-associated MAGs. This phylogenetic separation points to the potential existence of two disease-associated strains, each possibly linked to a distinct pathological progression.

In the tree generated using only high-quality MAGs (Figure 6.B), similar patterns emerge. A clear cluster associated with peri-implantitis remains identifiable, along with a smaller grouping of mucositis-related MAGs within the same branch. The relative distribution of host conditions remains largely consistent between the full dataset and the high-quality subset, indicating that increasing the resolution of the phylogenetic analysis does not drastically alter the observed clustering patterns. This consistency may be due, in part, to the limited number of available MAGs.

However, further interpretation is constrained by the imbalance and incompleteness of metadata, with only four healthy samples compared to thirteen each for mucositis and peri-implantitis. As a result, more in-depth statistical analyses are not feasible under the current dataset limitations.

## Conclusion

This study provides a comprehensive genomic and phylogenetic overview of Peptostreptococcus stomatis using 30 MAGs derived from oral samples linked to distinct health conditions. Quality assessment confirmed the inclusion of high- and medium-quality genomes, revealing minimal GC variation and consistent taxonomy. Functional analysis indicated that only ~34% of genes had known functions, emphasizing the underexplored nature of this species. The open pangenome structure and large accessory genome suggest high genomic plasticity and adaptability. Phylogenetic trees highlighted distinct clusters potentially associated with mucositis and peri-implantitis, while a separate group appeared commensal. Though further statistical validation is limited by sparse metadata and the low number of MAGs, these findings point to the presence of multiple strains with differing ecological roles. Overall, this work enhances our understanding of oral microbiota composition and lays a foundation for future studies linking microbial genomics to host health outcomes.

## References

[1] Downes J, Wade WG. Peptostreptococcus stomatis sp. nov., isolated from the human oral cavity. Int J Syst Evol Microbiol. 2006 Apr;56(Pt 4):751-754. doi: 10.1099/ijs.0.64041-0. PMID: 16585688.

[2] Huerta-Cepas, J., Serra, F., & Bork, P. (2016). ETE 3: Reconstruction, analysis, and visualization of phylogenomic data. Molecular Biology and Evolution, 33(6), 1635–1638. https://doi.org/10.1093/molbev/msw046

[3] Katoh, K., Rozewicki, J., & Yamada, K. D. (2017). MAFFT online service: multiple sequence alignment, interactive sequence choice and visualization. Briefings in Bioinformatics, 20(4), 1160–1166. https://doi.org/10.1093/bib/bbx108

[4] Löytynoja, A. (2013). Phylogeny-aware alignment with PRANK. Methods in Molecular Biology, 155–170. https://doi.org/10.1007/978-1-62703-646-7_10

[5] Medini, D., Donati, C., Tettelin, H., Masignani, V., & Rappuoli, R. (2005). The microbial pan-genome. Current Opinion in Genetics & Development, 15(6), 589–594. https://doi.org/10.1016/j.gde.2005.09.006

[6] Page, A. J., Cummins, C. A., Hunt, M., Wong, V. K., Reuter, S., Holden, M. T., Fookes, M., Falush, D., Keane, J. A., & Parkhill, J. (2015). Roary: rapid large-scale prokaryote pan genome analysis. Bioinformatics, 31(22), 3691–3693. https://doi.org/10.1093/bioinformatics/btv421

[7] Parks, D. H., Imelfort, M., Skennerton, C. T., Hugenholtz, P., & Tyson, G. W. (2015). CheckM: assessing the quality of microbial genomes recovered from isolates, single cells, and metagenomes. Genome Research, 25(7), 1043–1055. https://doi.org/10.1101/gr.186072.114

[8] Schwarz F, Derks J, Monje A, Wang HL. Peri-implantitis. J Clin Periodontol. 2018 Jun;45 Suppl 20:S246-S266. doi: 10.1111/jcpe.12954. PMID: 29926484.

[9] Seemann, T. (2014). Prokka: rapid prokaryotic genome annotation. Bioinformatics, 30(14), 2068–2069. https://doi.org/10.1093/bioinformatics/btu153

[10] Segata, N., Börnigen, D., Morgan, X. C., & Huttenhower, C. (2013). PhyloPhlAn is a new method for improved phylogenetic and taxonomic placement of microbes. Nature Communications, 4(1). https://doi.org/10.1038/ncomms3304

[11] Valm AM. The Structure of Dental Plaque Microbial Communities in the Transition from Health to Dental Caries and Periodontal Disease. J Mol Biol. 2019 Jul 26;431(16):2957-2969. doi: 10.1016/j.jmb.2019.05.016. Epub 2019 May 17. PMID: 31103772; PMCID: PMC6646062.