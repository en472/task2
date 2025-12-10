# import libraries

import subprocess
import argparse
import sys

# establish the program

def run_pipeline():
    # set up
    parser = argparse.ArgumentParser(description = 'run files through variant callers bcftools and snippy, and combine outputs')
    parser.add_argument('ref_genome', help = 'Reference genome')
    parser.add_argument('fq1', help = 'fastq reads 1')
    parser.add_argument('fq2', help = 'fastq reads 2')
    args = parser.parse_args()
    
    ## ========================================== RUN MINIMAP2/BCFTOOLS FIRST ====================================================
    
    # ------------------------------------ create conda environment specific for bcf tools ---------------------------------------
    print("creating conda environment for minimap/bcf tools route...")
    p1 = subprocess.run(
        'conda create -y -n bcf -c bioconda -c conda-forge minimap2 samtools bcftools bedtools',
        # run in shell
        shell=True,
        # capture the output
        capture_output=True,
        # display as readable text
        text=True
    )
    
    # ---------------------------------------------------- error checking --------------------------------------------------------
    
    # error handling (returncode = 0 when there are errors)
    if p1.returncode != 0:
        print("Error creating minimap/bcf environment:")
        # print the error output from p1
        print(p1.stderr)
        # exit program
        sys.exit(1)
    
    print("minimap/bcf conda environment created successfully")
    
    # -------------------------  run the minimap2 + samtools + bcftools pipeline as one bash command  ---------------------------
    
    print("\nrunning minimap/bcftools variant caller pipeline...")
    
    # create new string variable for the pipeline (explained in readme file)
    pipeline_cmd = f'''conda run -n bcf bash -c ' 
    minimap2 -a -x sr {args.ref_genome} {args.fq1} {args.fq2} | \
    samtools sort -O bam | \
    bcftools mpileup -Ou -f {args.ref_genome} - | \
    bcftools call -vc -Ov > bcf_vcf.vcf
    '
    '''

    # now run the string as a piped command in bash
    result = subprocess.run(
        pipeline_cmd,
        # make it run in shell
        shell=True,
        # capture the output
        capture_output=True,
        # as human readable text
        text=True
    )
    
    # ----------------------------------------------------- error checking -----------------------------------------------------------
    
    # check for errors in the pipeline
    if result.returncode != 0:
        print("\nError: minimap/bcf pipeline failed")
        sys.exit(1)
    
    # Check if output file was created 
    import os
    if not os.path.exists('bcf_vcf.vcf'):
        print("\nError: minimap/bcf output file not created")
        sys.exit(1)
    
    # use os package to get the size of the vcf file
    file_size = os.path.getsize('bcf_vcf.vcf')
    
    # checking that there is stuff in the file
    if file_size == 0:
        print("\nError: minimap/bcf output file is empty")
        sys.exit(1)
    
    print(f"first pipeline complete")
    
    
    ## ==================================================== RUN SNIPPY ==============================================================

    # ------------------------------------ create conda environment specific for snippy ---------------------------------------------
    print("creating conda environment for snippy route...")
    p1 = subprocess.run(
        'conda create -y -n snip -c bioconda -c conda-forge python==3.7.0 samtools bcftools bedtools snpEff==4.3 snippy==3.2 minimap2',
        shell=True,
        capture_output=True,
        text=True
    )
    
    # update the samtools version (not sure why but this worked on CLIMB terminals)
    samtools_downgrade = f'''conda run -n snip bash -c 'conda install samtools==1.3' '''
    
    # run the downgrade
    p2 = subprocess.run(
        samtools_downgrade,
        shell = True,
        capture_output = True,
        text = True
    )
    
    # ------------------------------------------------------ error checking ---------------------------------------------------------
    
    # error handling (returncode = 0 when there are errors)
    if p1.returncode != 0 | p2.returncode != 0:
        print("Error creating snippy environment:")
        # print the error output from p1
        print(f'' + p1.stderr)
        print(f'' + p2.stderr)
        # exit program
        sys.exit(1)
    
    print("snippy conda environment created successfully")
    
    # ------------------------------------------------------- run the snippy pipeline ---------------------------------------------------

    print("\nrunning snippy variant caller pipeline...")
    
    # create new string variable for the pipeline (explained in readme file)
    pipeline_cmd = f'''conda run -n snip bash -c ' 
    snippy --outdir snippy_results --ref {args.ref_genome} --R1 {args.fq1} --R2 {args.fq2}
    '
    '''

    # now run the string as a piped command in bash
    result = subprocess.run(
        pipeline_cmd,
        # make it run in shell
        shell=True,
        # capture the output
        capture_output=True,
        # as human readable text
        text=True
    )
    
    # ----------------------------------------------------- error checking -----------------------------------------------------------
    
    if result.returncode != 0:
        print("\nERROR: Snippy pipeline failed!")
        sys.exit(1)
    
    if not os.path.exists('snippy_results'):
        print("\nERROR: Output directory was not created!")
        sys.exit(1)

# set up to run when called on command line
if __name__ == "__main__":
    run_pipeline()