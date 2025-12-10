# Part 2 Results

## Overview:
Part 2 involves creating a pipeline to repeat the type of analysis performed in part 1 with two difference variant callers (bcftools and snippy), and comparing them. The same genomes (Plasmodium falciparum and Eschericia Coli) were used as before, where the PF data is simulated (from a real genome), and the Ecoli data is from real illumna reads. 

## Running the Pipeline:
The pipeline can be run on Linux machines using

  > python3 pipeline.py ref.fasta reads1.fastq reads2.fastq

The pipeline with indicate which stage it is running based on printed statements such as: 'creating conda environment for minimap/bcf tools route...'

## Output:

The bcftools section of the pipeline with output a VCF file called bcf_vcf.vcf into the same directory it was run in. Snippy, however, will open a new directory called 'results' which will contain a large number of files. The 'snps.vcf' file contains the detected mutations, and is the most important for this project. vcf_combine was then used to combine the output from both variant callers into one file. Where variant callers picked up different mutations at the same point, both were included, one after the other. 

The files from running both the real E.coli data and the simulated P. falciparum data are available in Part2_Data.

## Discussion:

It is difficult to determine how differently the two variant callers perform without physically trawling through the data. Direct comparison of the 'quality scores' for each mutation identified are not easily comparable as they hae different methods of scoring quality. Generally, both variant callers picked up the same snps, although returned quite different results for INDELS, presumably as these are more complex to identify. 




