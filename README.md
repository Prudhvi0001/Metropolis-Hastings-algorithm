## Part 1:  Part-of-speech tagging
### Problem:
Find the parts of speech tags for a new sentence given you have a labelled data with pos tags already.

Given Parts of Speech (12) :
```python
['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
```

Different Models Used:

### 1. Simple

##### Training 

Find the count of all pos tags occurring for each word and find their Probabilities 

( This is used for finding the pos tags using simple model)

To perform part-of-speech tagging, we want to estimate the most-probable tags for each word Wi,

$$
s∗i= arg maxsi P(Si=si|W).
$$

Ex:

| Words   | 'adv' | 'adj' | 'verb' | .................. |
| ------- | ----- | ----- | ------ | ------------------ |
| The     | 10    | 2     | 3      | ................   |
| Prudhvi | 2     | 4     | 6      | ........           |
| Anji    | 3     | 5     | 4      | .........          |
| Ruthvik | 6     | 6     | 2      | .............      |

Similarly find their Probability table by Dividing wrt each column.

#### Testing

Take the maximum occurred pos tag for each word in the given sentence. 
If the is not their in training data set label it as noun (As nouns are the most common occurences for a new data point as all other pos tags are general occuring tags) and accuracy is also good :-)

### 2.HMM Viterbi

##### Training

Calculate the Emission and Transition  Probability tables

Emission Table:

Probability of Occurrence of a word given pos tag  P(tag = 't1'/word)

 if their zero probability give it a probability of 0.000000000001

| Words        | tag1           | tag2           | tag3 | ........ |
| ------------ | -------------- | -------------- | ---- | -------- |
| w1           | p(tag = t1/w1) | p(tag = t2/w1) | ...  | .......  |
| w2           | ..             | ..             | ..   | ..       |
| w3           | ....           | .              | .    | .        |
| ............ | .              | .              | .    | .        |

Transition Probability:

Probability of P(pos_tag2/pos_tag1)

Ex: P('noun'/'noun')

#### Testing
find the maximum a posteriori (MAP) labeling for the sentence

$$
(s∗1, . . . , s∗N) = arg   maxs1,...,sNP(Si=si|W).
$$

We can solve this model by using viterbi (Dynamic Programming) using transition and emission probabilities to calculate the maximun occuringsequence 


### 3.Complex_MCMC (Gibbs Sampling)

##### Training
Use the probability tables from previous viterbi and separetley caluculate the probaility of P(Sn/Sn-1,s0)


#### Testing

Initialize the word pos sequence to some random pos tags # Here I Initialized it to nouns.
Using Gibbs sampling sample the Probabilities each word by making all other values constant and after the healing period store the maximum occured sequences counts in a dictionary.

After sampling output the maximum occurred sequence for each word.

Testing Accuracies:

</b>Note: Accuracies for complex model may vary during runs as it takes random samples.</b>

For bc.test

| Models        | Words correct: | Sentences correct: |
| ------------- | -------------- | ------------------ |
| Ground truth: | 100.00%        | 100.00%            |
| Simple:       | 93.95%         | 47.50%             |
| HMM:          | 95.09%         | 54.40%             |
| Complex:      | 95.05%         | 54.30%             |

For bc.test.tiny

| Models        | Words correct: | Sentences correct: |
| ------------- | -------------- | ------------------ |
| Ground truth: | 100.00%        | 100.00%            |
| Simple:       | 97.62%         | 66.67%             |
| HMM:          | 97.62%         | 66.67%             |
| Complex:      | 100.00%        | 100.00%            |


#### Posterior Probabilites:

### Simple:
   Calculate the Posterior Probabilities of simple model as P = p(word/tag)*p(tag)
   
### HMM:
   For HMM model P = p(word/tag)*prob(tag/prev_tag)
   
### Complex_mcmc
   Calculate the Posterior Probabilities of complex model as P = p(word/tag)*p(tag/prev_tag)*p(next_tag/tag)


# Part 2 : Code Breaking :

 The procedure I have followed for code breaking is , firstly I have extracted the transition probabilities from the corpus for each letter  i.e basically normalizing frequencies by count and according to the metropolis-hasting algorithm, I have randomly generated replace and rearrange tables and used those tables for decoding the encrypted text and calculated P(D) using the decrpyted text and copus's transition probabilities , which tells us how english likely is the decrypted text .Later , I have updated the the tables, each with  a 50 % chance of getting updated and now used them from decrpyting the encrypted text and then using the decrpyted text and corpus's transition probabilities , I have caluclated P(D') for modified tables. <br><br>
            If P(D') > P(D) , i'm replacing the previous tables with these modified tables. If P(D) > P(D') , then I'm updating the tables with a probability of P(D')/P(D) by randomly generating the probability values by using numpy.rondom.binomial function which randomly generates probability for 1 trial and check if it's value is less than P(D')/P(D) , if it is less then returns 1 else returns 0 .So,based on this chance I will either update or discard the new/modified tables . <br><br>
          But, unfortunately I was unable to decrypt the text correctly , I have tried many approaches such as updating only rearranging tables witha  prob of less than 0.4, updating only replace tables with a prob of  0.4 - 0.7 and for probability greater than 0.7 ,I've updated both , also tried updating both on each iteration by random shuffling rearranging tables and also by shuffling 3,4,5 mappings in
replace tables .


 # Part 3: Naive Bayes Classifier

We have solved the problem using:
-> Naive Bayes Classifier

The Procedure ::

We are taking the inputs using System Arguments ::
Training Directory = sys.argv[1]
Testing Directory = sys.argv[2]
Output+File_Name = sys.argv[3]

The first argument takes a Training Directory .
The Second Argument Takes a Testing Directory.
The third Argument Takes a File Name to print the formatted Output.


->Make_dict():
  Used this function to create::
  1.)Spam Data Dictionary
  2.)Not Spam Data Dictionary
  
  To Calculate the Total Number of ::
  a.)Positive Word Count.
  b.)Negative Word Count.
  c.)Spam Files.
  d.)Not Spam Files.
  
 ->Calculate Probability():
  Used this function to apply naive bayes classifier on the processed input data.
  
  Used the Naive Bayes Formula ::
  
  P(A|b) = P(B|A)P(A) / P(B)
  
 ->Accuracy ::
  Initially after writing the code and analyzing the accuracy , the accuracy wasn't optimal.
  
  Then we had to implement Pre-processing of the Input Data.
  
  As part of Pre-processing we removed::
  * Escape Sequences
  * Special Characters
  * Lower()
  * Stop Words
  
  Probability_Spam =(spam_total) / (spam_total + notspam_total)
  Probability_Not_Spam = (notspam_total) / (notspam_total + spam_total)
  
  Observations::
  **Without Any Pre-processing the Accuracy was ::
      The Spam Filter Accuracy is :: 97.65074393108848
      
     After Considering only ::
     $ Remove Escape Sequence
     $ lower()
     $ remove stop words
     
     The Finaly Accuracy when compared to the Ground Truth ::
        The Spam Filter Accuracy is :: 98.70790916209867
        
    
    
    **Hence our Spam Filter was able to get an Accuracy of ::98.70790916209867**
     
     
   
  
  
  
  
  
  
  
  
  
