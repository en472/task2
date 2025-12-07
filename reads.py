
# put this into a function, need to find out how to do this in commadn line so that output is in a .txt file that can be sent to another program
# would be cool to have inputs as: filename, read depth, and read length!!!!
# generating reads

# libraries
import random

# read in testing sequences
with open('mutated_sequence.txt', 'r') as file:
    # remove the first line
    id = next(file)
    seq = file.read()

seq = seq.replace('\n', '')

# set read lengths
read_length = 100

# set no of reads
no_of_reads = 630000 # for 30x depth

# select 5 random points

# make index
point_index = list(range(1, len(seq)))

# select random points from the index
points = random.choices(point_index, k = no_of_reads) # this can choose the same point multiple times

# reset points at end to make sure full reads are found (no shorter reads from choosing a point too close to the end of the sequence)
# select the index of points which go over the boundary
points_to_edit = [point for point in range(len(points)) if points[point] > (len(seq) - read_length)]

# edit those points to a set value (latest before the read hangs over the edge)
for index in points_to_edit:
    points[index] = len(seq) - read_length

# use the points to extract out a read length of 100 bases - list comprehension
reads = [seq[point:point + read_length] for point in points] 

# now write reads into a .txt file
#with open('reads.txt', 'w') as file:
 #   file.writelines(line + '\n' for line in reads)
    
    
# edit the id header to reformat
id = '@' + id[1:-1]

read_number = 1

quality_scores = ''.join(random.choices(')*%.!', k = 100))

with open('reads.fq', 'w') as file:
    for line in reads:
        file.write(id + '_' + str(read_number) + '\n')
        read_number = read_number + 1
        file.write(line + '\n')
        file.write('+\n')
        file.write(quality_scores + '\n')




