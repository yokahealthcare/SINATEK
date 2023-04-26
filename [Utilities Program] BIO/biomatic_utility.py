# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 14:10:25 2021

BIOINFORMATICS LIBRARY
@author: Erwin

"""

from prettytable import PrettyTable
import matplotlib.pyplot as plt

"""
Function to count matched pattern in DNA
ARGUMENTS:
Pattern = "ATA"
Text = "CGATATATCCATAG"
"""
import re
def patternCountEfficient(genome, pattern):
  return len(re.findall("(?=%s)" % pattern, genome))

# THIS IS SAME

def patternCount(genome, Pattern):
    count = 0
    for i in range(len(genome)-len(Pattern)+1):
        if genome[i:i+len(Pattern)] == Pattern:
            count = count+1
    return count 

# THIS IS SAME + POSITIONS WHEN MATCHING OCCURS

# fill in your PatternMatching() function along with any subroutines that you need.
def patternMatching(Genome, Pattern):
    positions = [] # output variable
    len_genome = len(Genome)
    len_pattern = len(Pattern)
    
    for i in range(len_genome - len_pattern +1):
      new_Pattern = Genome[i:i+len_pattern]
      if  new_Pattern == Pattern:
        positions.append(i)

    return positions

"""
Function to make reverse complement DNA 
ARGUMENTS:
Pattern = "ATCGCTATT"
"""

# Input:  A DNA string Pattern
# Output: The reverse complement of Pattern
def reverseComplement(Pattern):   
    return reverse(complement(Pattern))

# Copy your Reverse() function here.
def reverse(Pattern):
    return Pattern[::-1]

# Copy your Complement() function here.
def complement(Pattern):
    compl = {"A":'T', "T":'A', "C":'G', "G":'C'}
    completed = ""
    for i in Pattern:
        completed += compl[i]
    return completed

"""
Function to make check frequency of pattern on DNA 
ARGUMENTS:
Text = "CGATATATCCATAG"
Complemented = "GCTATATAGGTATC"
Reversed = "CTATGGATATATCG"
"""

def frequencyMap(ORI, kmers):
    freq = {}
    n = len(ORI)
    for i in range(n-kmers+1):
        Pattern = ORI[i:i+kmers]
        freq[Pattern] = patternCountEfficient(ORI, Pattern) 
    
    return freq

""""
how to select the value of k that results in the "most surprising" frequent k-mer.
"""
def print_kmers_occurance(ORI):
    field_names = [
        "K", "3", "4", "5", "6", "7", "8", "9"
    ]
    x = PrettyTable(field_names)
    occurance_data = ["Occurance"]
    kmers_data = ["K-mers"]
    
    for i in range(3,10):
        storage = frequencyMap(ORI, kmers=i)
        m = max(storage.values())
    
        gen = ""
        for k,v in storage.items():
          if v == m:
            gen += k + "\n"
        
        occurance_data.append(m)
        kmers_data.append(gen)
    
    x.add_row(occurance_data)
    x.add_row(kmers_data)
    print(x)

"""
Function to get the frequency of Symbol on specific symbol on the genome
ARGUMENTS:
Genome = "CGATATATCCATAG"
Symbol = "C" / "A" / "T" / "G" 
"""

def fasterSymbolArray(Genome, symbol):
    array = {}
    n = len(Genome)
    ExtendedGenome = Genome + Genome[0:n//2]

    # look at the first half of Genome to compute first array value
    array[0] = patternCount(symbol, Genome[0:n//2])

    for i in range(1, n):
        # start by setting the current array value equal to the previous array value
        array[i] = array[i-1]

        # the current array value can differ from the previous array value by at most 1
        if ExtendedGenome[i-1] == symbol:
            array[i] = array[i]-1
        if ExtendedGenome[i+(n//2)-1] == symbol:
            array[i] = array[i]+1
    return array

""""
plotting the result from the previous function.
To find the ORI location of replication
"""

"""
FROM : Stepik Course
The figure below visualizes the symbol array for E. coli and symbol equal to "C". Notice the clear pattern in the data! The maximum value of the array occurs around position 1600000, and the minimum value of the array occurs around position 4000000. We can therefore infer that the reverse half-strand begins around position 1600000, and that the forward half-strand begins around position 4000000. Because we know that ori occurs where the reverse half-strand transitions to the forward half-strand, we have discovered that ori is located in the neighborhood of position 4000000 of the E. coli genome, without ever needing to put on a lab coat!
"""

def plotSymbolArray(genome_file_path, symbol):
    with open(genome_file_path) as file:
        genome_loaded = file.read();

    array = fasterSymbolArray(genome_loaded, symbol)
    
    plt.plot(*zip(*sorted(array.items())))
    plt.show()
