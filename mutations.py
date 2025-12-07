
# inserting mutations into the genome

# import libraries/toolkits
import random
from itertools import repeat

# ============================================================ Set up =============================================================

# assign insertions/deletions split
n_dels = random.randrange(0, 20)
n_ins = 20 - n_dels

# read in sequence
with open('NC_037282.1.fasta', 'r') as file:
    # save the first line as 'id'
    id = next(file)
    # read the rest of the file in as the sequence
    seq = file.read()

# remove newline characters from the input sequence
seq = seq.replace('\n', '')

# create an index for the sequence (starting from 1)
index = list(range(1, len(seq) + 1, 1))

# establish dictionary for recording changes made to the sequence
change_log = {}

# ========================================================== Deletions =============================================================

# loop over once per deletion
for no_of_del in range(0, n_dels):

     # select a random point from the index
    point = random.choice(index[:-1])
    
    # find the index value of the point in the genome selected
    point_index = index.index(point)
    
    # generate a random length for deletion (1-10bp)
    del_length = random.randrange(1, 10)
    
    # select the section of the sequence to be deleted (del_seq)
    if ((point_index + del_length) > len(seq)):
        del_seq = seq[point_index:]
    # ^^ above is for if the deletion sequence will overhang the end of the sequence, it will delete up to the end
    else:
        del_seq = seq[point_index:point_index + del_length]
        
    # save the index point (remove 1 for readability), the change type, and the sequence removed into the dict
    change_log[point - 1] = ('del', seq[point_index - 1] + del_seq, seq[point_index - 1])
    
    # delete the sequence by the point index
    seq = seq[:point_index] + seq[point_index + del_length:]
    
    # delete corresponding index numbers to update the reference index
    index = index[:point_index] + index[point_index + del_length:]
    

# ========================================================== Insertions =============================================================

# initialise available base choices for insertions
base_choices = 'AGCT'

# loop over for number of insertions
for no_of_ins in range(0, n_ins):
    
    # remove 0 values prior to insertion point selection (to prevent insertions within insertions)
    filtered_index = [i for i in index if i != 0] 
    
 # ---------------------------------------------------- build the insertion sequence --------------------------------------------   
    
    # generate the length of the insertion sequence (1-10bp)
    insertion_sequence_length = random.randrange(1, 10)
    
    # set up empty variable for insertion sequence
    insertion_sequence = ''
    
    # loop over for length on insertion
    for i in range(0, insertion_sequence_length):
        
        # select a random base from available choices
        random_base = random.choice(base_choices)
        
        # append the base to the insertion sequence
        insertion_sequence = insertion_sequence + random_base
        
# ----------------------------------------------------- insert the sequence --------------------------------------------------------    

    # select a random point in the genome using the index
    point = random.choice(filtered_index[:-1])
    
    # find the index value of the point
    point_index = index.index(point)
    
    # save the index point, the change type, and the sequence inserted into the dict
    change_log[point] = ('ins', seq[point_index], seq[point_index] + insertion_sequence)
    
    # insert the sequence into the genome using the point index
    seq = seq[:point_index + 1] + insertion_sequence + seq[point_index + 1:]
    
    # make sequence of 0s, the same length as the insertion sequence to update the reference index
    zero_list = [0] * insertion_sequence_length
    
    # insert list of zeros into index to indicate nucleotides which have been inserted (and are therefore removed from selection pool)
    index = index[:point_index] + zero_list + index[point_index:] 
    
# ============================================================ SNPs =====================================================================

# begin by filtering the index to indentify the available mutation pool
filtered_index = [i for i in index if i != 0]   

# ------------------------------------------------------- Generate SNPs ---------------------------------------------------------------

# select out 300 values from index 
points = random.sample(filtered_index, k = 300) 

# select out nulceotides which correlate to the points selected in the genome
bases_for_mutation = [seq[i] for i in points]

# generate random bases for snps
snps = random.choices('ACGT', k = 300)

# loop through 300 snps and re-select for ones which happen to be the same as the original genome
while any([a == b for a, b in zip(bases_for_mutation, snps)]) == True:
    for i in range(0, len(bases_for_mutation)): 
        if bases_for_mutation[i] == snps[i]:
            snps[i] = random.choice('ACGT')
            

# ------------------------------------------------------- Insert into Genome ----------------------------------------------------------

# set sequence to list data type
seq = list(seq)

# find matches between the points for mutation and the original unflitered index
matches = []

for i in range(len(points)):
    points_value = points[i]
    matches.append(index.index(points_value))


# empty list for bases changes for change log
snped_bases = []

# update sequence with SNPs at the mutation points (adjusted through matches to make sure that insertion points are not snped)
for i in range(0, len(snps)):
    # append to list of bases changed for change log
    snped_bases.append(seq[matches[i] + 1])
    # update sequence with changes at snp points
    seq[matches[i] + 1] = snps[i]
    
# ----------------------------------------------------- Update Change Log --------------------------------------------------------------

# join snps and original bases together for input into change log
snp_values_for_change_log = zip(repeat('snp'), snped_bases, snps)

# so that changelog counts from 1
points = [point + 1 for point in points]

# create dictionary for snps
snps_change_log = dict(zip(points, snp_values_for_change_log))

# update dictionary with snps
change_log.update(snps_change_log)

# ======================================================= Exporting Results ============================================================

# export the change log 
with open ('change_log.txt', 'w') as file: 
    for key, value in change_log.items():
        file.write(f"{key}: {value}\n")
    file.close()
    
# change sequence format
seq = ''.join(seq)

with open ('mutated_sequence.txt', 'w') as file:
    # include orignal header for metadata
    file.write(id)
    # write mutated sequence in lines of 70 characters (as in original format)
    for i in range(0, len(seq), 70):
        chunk = seq[i:i + 70]
        line = chunk + '\n'
        file.write(line)
    file.close()
    
   





    