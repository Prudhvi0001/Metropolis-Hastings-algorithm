#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: PLEASE PUT YOUR NAMES AND USERIDS HERE
#
# based on skeleton code by D. Crandall, 11/2019
#
# ./break_code.py : attack encryption
#


import random
import math
import copy 
import sys
import encode
import numpy as np
import time




def get_tran_prob(data):
    data_dict = {}
    curr_char = ""
    prev_char = "Start"
    data_list = [char for char in data ]
    for i in range(0,len(data_list)):
        curr_char = data_list[i]
        if curr_char not in data_dict.keys() :
             data_dict[curr_char] = {"count": 1}
        if prev_char in data_dict.keys():
            if curr_char in data_dict[prev_char].keys():
                data_dict[prev_char][curr_char] += 1
            else:
                 data_dict[prev_char][curr_char] = 1
            data_dict[curr_char]["count"] += 1
        prev_char = curr_char

    for alphabet,freq_dict in data_dict.items():
        freq_size = freq_dict["count"]
        for char,freq in freq_dict.items():
            prob = freq/freq_size
            data_dict[alphabet][char] = prob
    
        
    return data_dict
    

def caluclate_prob(trans_prob,string):
    
    total_prob = []
    word_list = string.split()
    for word in word_list:
        prev_char = ' '
        curr_char = ''
        prob = []
        for char in word:
            curr_char = char
            trans_dict = trans_prob[prev_char]
            if curr_char in trans_dict.keys():
                t_prob = trans_prob[prev_char][curr_char] 
                prob.append(math.log(t_prob))
            prev_char = curr_char
        total_prob.append(sum(prob))    
    return sum(total_prob)
    
    
def  get_decrypt_tables():
    letters=list(range(ord('a'), ord('z')+1))
    random.shuffle(letters)
    replace_table = dict(zip(map(chr, range(ord('a'), ord('z')+1)), map(chr, letters)))
    rearrange_table = list(range(0,4))
    random.shuffle(rearrange_table)

    return replace_table,rearrange_table


def get_updated_tables(replace_table1,rearrange_table1,string_trans_prob):
    prob = np.random.binomial(1,0.5)
    replace_table  =  copy.deepcopy(replace_table1)
    rearrange_table = copy.deepcopy(rearrange_table1)
    if (prob == 1) :
        i1 = random.randint(0,3)
        i2 = random.randint(0,3)
        rearrange_table[i1],rearrange_table[i2] = rearrange_table[i2],rearrange_table[i1]
    else:
        alphabet_list = [ alphabet for alphabet,trans_prob in string_trans_prob.items() if alphabet != 'count' and alphabet != ' ']
        index1 = random.randint(0,len(alphabet_list)-1)
        index2 = random.randint(0,len(alphabet_list)-1)
        index3 = random.randint(0,len(alphabet_list)-1)
        char1 = alphabet_list[index1]
        char2 = alphabet_list[index2]
        replace_table[char1],replace_table[char2] = replace_table[char2],replace_table[char1]
    return replace_table, rearrange_table
      

# put your code here!
def break_code(string, corpus , replace_table,rearrange_table,t):
    corpus_trans_prob = get_tran_prob(corpus)
    decode_string = encode.encode(string,replace_table,rearrange_table)     
    prob_decode_d = caluclate_prob(corpus_trans_prob,decode_string)
    count =0
    re_pl = {}
    re_ar = {}
    t1 = time.time()
    while time.time() - t1 < t:
      count += 1
      replace_table1,rearrange_table1 = get_updated_tables(replace_table,rearrange_table,corpus_trans_prob)
      decode_string1 = encode.encode(string,replace_table1,rearrange_table1)     
      prob_decode_d1 = caluclate_prob(corpus_trans_prob,decode_string1)
      
      if prob_decode_d > prob_decode_d1:
          prob = np.random.binomial(1,np.exp((prob_decode_d1 - prob_decode_d)/100))
          if (prob == 1):
              replace_table,rearrange_table = copy.deepcopy(replace_table1),copy.deepcopy(rearrange_table1)
              prob_decode_d = prob_decode_d1

      else:
           re_pl[prob_decode_d1] = replace_table1
           re_ar[prob_decode_d1] = rearrange_table1
           replace_table,rearrange_table = copy.deepcopy(replace_table1),copy.deepcopy(rearrange_table1)
           prob_decode_d = prob_decode_d1

           
    print(count)
    return decode_string,re_pl,re_ar


if __name__== "__main__":
   if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")

   encoded = encode.read_clean_file(sys.argv[1])                  
   corpus = encode.read_clean_file(sys.argv[2])      
   
   for i in range(0,8):
    max_p = -math.inf
    replace_table,rearrange_table = get_decrypt_tables()                        
    decoded,re_pl,re_ar = break_code(encoded, corpus,replace_table,rearrange_table,600)
    with open(sys.argv[3], "w") as file:                                                                                                                              
        print(decoded, file=file)
    for key,value in re_pl.items():
        if key > max_p:
            max_p = key
    replace_table = re_pl[key]
    reaarange_table = re_ar[key]
    decode_string = encode.encode(encoded,replace_table,rearrange_table)   
    with open('output_best_'+str(i)+'.txt', "w") as file:                                                                                                                              
        print(decode_string, file=file)
    
        

