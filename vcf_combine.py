
# combining vcfs into one!

def vcf_combine(vcf1, vcf2):

# read in vcf files

    with open(vcf1, 'r') as file:
        vcf1 = file.readlines()
        
    with open(vcf2, 'r') as file:
        vcf2 = file.readlines()
        

# remove headers and clean then to only extract results (same code as used in vcf_compare)
    # vcf1
    vcf1 = [line for line in vcf1 if not line.startswith('##')]
    
    vcf1 = vcf1[1:]
    
    vcf1_mutations = []
    # split by \t
    for i in range(0, len(vcf1)):
        first_cols = '\t'.join(vcf1[i].split('\t')[1:5])
        vcf1_mutations.append(first_cols)

    # replace \t
    vcf1_mutations = [entry.replace('\t', ' ') for entry in vcf1_mutations]
    
    # remove .
    vcf1_mutations = [entry.replace('.', '') for entry in vcf1_mutations]
    
    # vcf2
    vcf2 = [line for line in vcf2 if not line.startswith('##')]
    
    vcf2 = vcf2[1:]
    
    vcf2_mutations = []
    # split by \t
    for i in range(0, len(vcf2)):
        first_cols = '\t'.join(vcf2[i].split('\t')[1:5])
        vcf2_mutations.append(first_cols)

    # replace \t
    vcf2_mutations = [entry.replace('\t', ' ') for entry in vcf2_mutations]
    
    # remove .
    vcf2_mutations = [entry.replace('.', '') for entry in vcf2_mutations]
    
    
    # reconstruc the vcf with each only being included UNLESS is something as the same point, then choose at random
    print(vcf1_mutations[0].split('  ')[0]) # this is how we access the position numbers
    
     
    # split the values from the nucleotides
    for i in range(0, len(vcf1_mutations)):
        vcf1_mutations[i] = vcf1_mutations[i].split('  ')
    
    for i in range(0, len(vcf2_mutations)):
        vcf2_mutations[i] = vcf2_mutations[i].split('  ')
    
    # literally stack lists together
    combined_vcf = vcf1_mutations + vcf2_mutations  
    
    # order by origin point
    combined_vcf = sorted(combined_vcf, key = lambda x: int(x[0]))

    # remove exact duplicates
    unique_entries = []
    [unique_entries.append(x) for x in combined_vcf if x not in unique_entries]
    
    # write out as file
    with open('combined_vcf.vcf', 'w') as file:
        for line in unique_entries:
            file.write(str(line))
            file.write('\n')
        

vcf_combine('bcf_vcf.vcf', 'snps.vcf')