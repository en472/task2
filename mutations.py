
# making mutations =========

## libraries
import random

## decide on insertions / deletions split

n_dels = random.randrange(0, 20)
n_ins = 20 - n_dels

## create original index for sequence

test = 'AGCGTACAGTAGCTAT'

# label the string with an index for characters

index = list(range(1, len(test) + 1, 1))

# establish dictionary for changes to sequence
change_log = {}

#  deletions

print(test)

# problem -  needs to take the position of the number in the index and use that to decide where to delete from, not the value itself - otherwise you can end up with blank values in the change-log from poor deletions.
# loop over once for each deletion (as generated previously) - for now, this sometimes errors if the sequencs taken are too large for the example, but this shouldn't occur in the full genome. Test it out!
for no_of_del in range(0, n_dels):
    
    # select a random point in the genome using the index
    point = random.choice(index[:-1])
    
    point_index = index.index(point)
    print(point_index) ## this is two less  than point for some reason
    
    # generate a random length for deletion (1-10bp)
    del_length = random.randrange(1, 10)
    
    # select the sequence to be deleted
    if ((point + del_length) > len(test)):
        del_seq = test[point:] # for if the deletion overhangs the sequence
    else:
        del_seq = test[point:point + del_length]
    
    # save the index point, the change type, and the sequence removed into the dict
    change_log[point + 1] = ('del', del_seq)
    
    # delete the sequence
    test = test[:point] + test[point + del_length:]
    
    print(change_log)
    print(test)
    
    # delete corresponding index numbers to update
    index = index[:point] + index[point + del_length:]
    print(index)

    
# loop over range for insertions - works but same problem as del, indexing by point rather than from posotion of point, need to adjust insertion points so everything lines up and 
for no_of_ins in range(1, n_ins):
    
    # select a random point in the genome using the index (after deletions)
    point = random.choice(index[:-1])
    
    # generate a random sequence for insertion (1-10bp)
    insertion_sequence_length = random.randrange(1, 10)
    
    insertion_sequence = ''
    
    base_choices = 'AGCT'
    
    for i in range(0, insertion_sequence_length):
        random_base = random.choice(base_choices)
        
        insertion_sequence = insertion_sequence + random_base
        
    # select the point of insertion
    point = random.choice(index)
    
    # save the index point, the change type, and the sequence inserted into the dict
    change_log[point + 1] = ('ins', insertion_sequence)
    
    # insert the sequence? (ad this earlier)
    test = test[:point] + insertion_sequence + test[point:]
    
    # make index insertion sequence
    zero_list = [0] * insertion_sequence_length
    
    # insert corresponding 0 index numbers to update
    index = index[:point] + zero_list + index[point:] 
    
    print(test)
    print(change_log)
    print(index)
    


# SNPs

# iterate through non-zero index values

# select random non-zero value in index
# find relative position in sequence

# update change log dict 

# add SNP

# update index value to 0, to remove it from the selection pool each round


## output file