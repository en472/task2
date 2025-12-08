# Part 1 Results

## Overview:
The Plasmodium falciparum Strain 3D7 Chromosome 11 sequence and whole genome sequence of Escherichia coli Strain K-12 (Substrain MG1655) were mutated by the mutations() function written in mutations.py. 20 INDELS (randomly assigned) and 300 SNPs were applied to each sequence, and all mutations were recorded in a change log. The reads() function described in reads.py was then used to simulate 30x depth of 100bp reads accross both sequences, and saved in FASTQ format with randomised base quality. These reads were compressed via the gzip tool, and then mapped to the original genome (used as reference) via minimap2 which generated BAM files. Next, pileups were generated using bcftools which yielded VCF files containing the detected mutations. The VCF files were compared with the 'truth' change logs via vcf_compare() in vcf_compare.py, to generate estimates of both precision and recall. Finally, these estimates were interrogated by manally searching for mutations in the BAM files, and visualising via samtools. 

## Results:

The VCF files from Escherichia coli Strain K-12 had a precision of 43.75% and a recall of 46.25%. This implies that less than half of the simulated mutations were detected by the variant caller, which is mediocre performance. Similarly, Plasmodium falciparum Strain 3D7 had precision 56.25% and recall 58.75%. 

The reads from both genomes were mapped successfully. All 1,380,000 Ecoli and 60,000 Plasmodium reads passed QC when interrogated with samtools flagstat, and the percentage of sucessfully mapped reads was 100% and 99.76% respectively. We can therefore assume that these low detection rates are not due to errors in the mapping process, and are more likely due to missed/inaccurate detections during bcftools pileup stage, or may be due to errors in vcf_compare(). 

## Comparing Truth vs. Detected Mutations:

When viewing the indexed BAM file, it is difficult to understand why some SNP mutations were not included in the VCF file. For example, the change log for Ecoli shows there was a SNP mutation at nucleotide 49468:

<img width="318" height="190" alt="Screenshot 2025-12-08 155808" src="https://github.com/user-attachments/assets/70983218-6d35-4987-9957-672436a1066d" />

Yet there is no record in the VCF file.

<img width="369" height="178" alt="Screenshot 2025-12-08 155854" src="https://github.com/user-attachments/assets/40a2317d-f6e5-4d2f-9a48-4e15f24913ee" />

When observing point 49468 in the samtools pileup terminal view, we can see that there does appear to be a SNP mutation at the location, from a 'C' to 'A', as listed in the change log.

<img width="396" height="835" alt="image" src="https://github.com/user-attachments/assets/44d1d85b-10ff-4e04-847b-bc09a223dad7" />

Unfortunately, there is little clear reason why this change was not recorded in the VCF file, as every read mapped to this portion of the genome contains the SNP mutation C -> A. It may be that there were just not enough reads (this nucleotide had depth 31) for the program to be certain, and therefore it was not included in the final VCF.

Otherwise, the varient caller seems to have detected INDELs successfully, in both Plasmodium:

<img width="435" height="216" alt="image" src="https://github.com/user-attachments/assets/d3ce6d93-85f9-48f7-836c-d496ed21ba72" />

<img width="378" height="730" alt="image" src="https://github.com/user-attachments/assets/11b7e3e8-3bf5-4f21-8179-ca15bf2d5632" />

And in E coli:

<img width="436" height="130" alt="image" src="https://github.com/user-attachments/assets/a4c23909-f07e-487f-a569-1d1af781431b" />

<img width="327" height="752" alt="image" src="https://github.com/user-attachments/assets/aed27a7c-a0e9-4639-8f15-a0d3c3d64f86" />

## Data Access
As each run of this pipeline produces different random mutations, the files used for this specific run are available in folder Part1_Data for reproducibility. (the FASTQ files could not be included as they are too large for Github, but a screenshot of the first few Plasmodium reads is shown below:)

<img width="1251" height="420" alt="image" src="https://github.com/user-attachments/assets/6f6e59e2-7e28-4736-9a70-fd707cff6da8" />


