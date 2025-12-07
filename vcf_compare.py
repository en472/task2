
import re

# read in vcf file

with open('test.vcf', 'r') as file:
    vcf = file.readlines()

# remove header lines
vcf = [line for line in vcf if not line.startswith('##')]

# remove table header line
vcf = vcf[1:]

# extract only the first few columns of each header
detected_mutations = []

# split by \t
for i in range(1, len(vcf)):
    first_cols = '\t'.join(vcf[i].split('\t')[1:5])
    detected_mutations.append(first_cols)

# replace \t
detected_mutations = [entry.replace('\t', ' ') for entry in detected_mutations]

# remove .
detected_mutations = [entry.replace('.', '') for entry in detected_mutations]

#print(detected_mutations)

# read in changelog
with open('change_log.txt', 'r') as file:
    log = file.readlines()
    
# remove newlines
log = [entry.replace('\n', '') for entry in detected_mutations]

# remove special characters
log = [re.sub(r'[^a-zA-Z0-9]', ' ', entry) for entry in log]

#print(log)

# set number of matches
correct_matches = 0

# compare log and detected mutations line by line
for line in range(0, len(log)):
    if log[line] == detected_mutations[line]:
        correct_matches = correct_matches + 1
        
# calculate % of matches correct (precision)
precision = correct_matches / len(log) * 100

# calculate number of mutations found relative to actual number (recall)
recall = len(detected_mutations) / len(log) * 100

print(f'precision: ', precision)

print(f'recall: ', recall)
