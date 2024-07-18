# Julius Quiaot - Illumio Technical Assessment

This repository contains the results of attempting Illumio's technical
assessment.

## Problem Statement

The problem statement, as per the email instructions (minor formatting fixes introduced):

Task 1: Description: Write a program that reads a file and finds matches
against a predefined set of words. There can be up to 10K entries in the list
of predefined words. The output of the program should look something like this:

```
Predefined word           Match count 
FirstName                        3500 
LastName                         2700 
Zipcode                          1601 
```

Requirement details:

* Input file is a plain text (ascii) file, every record separated by a new line.
* For this exercise, assume English words only 
* The file size can be up to 20 MB 
* The predefined words are defined in a text file, every word separated by a
  newline. Use a sample file of your choice for the set of predefined keywords
  for the exercise.
* Assume that the predefined words file doesn’t contain duplicates 
* Maximum length of the word can be upto \[sic\] 256 
* Matches should be case-insensitive
* The match should be word to word match, no substring matches.
* Consider a sample file with only the following two lines:

Line 1: Detecting first names is tricky to do even with AI. 
Line 2: how do you say a street name is not a first name?

And a sample list of predefined words: 

Name 

Detect 

AI 

The match should happen only for the word “AI” in the first line and the word
“name” in the second line.  The word “Detect” should not match.

If there is any aspect of the requirement or question is not clear, please make
reasonable assumptions and document them in the README file to be submitted
with the assignment.

## Discussion

* Working with two files here:
  * Word file (dictionary) - a list of words, one word per line, used to match
	* Up to 10k words (entries)
	* Constrain to alphanumeric characters, no spaces
  * Content file - a file containing records, each record separated by a newline
	* Up to 20MB
	* Content appears to be arbitrary sentences or snippets, can be of any case,
	  may contain punctuation, different case
  * Word matching
	* Whole words only
	* Case-insensitive

Initial thoughts on approach: Since we are looking at exact, case-insensitive
matches only, and with a dictionary size of up to 10k, it's not unreasonable
as a first approach to use a simple map/dict to count the number of occurrences
of the words in our dictionary.

If we wanted to do partial word matches, or if the number of words we need to
match against was larger, we might want to explore using something like a prefix
tree (trie) to capture the match words.

Output appears to be in descending order from most to least number of occurrences,
so we'll try to format the output accordingly.

We'll count number of occurrences of each word throughout the entire corpus, rather
than the number of records containing each word.

Test words generated from: https://randomwordgenerator.com/

Test content/records generated from https://randomwordgenerator.com/sentence.php

Basic algorithm outline:

Dictionary generation:

```
* Parse word file line by line
* For each word
  * Convert to lowercase
  * Add it to dictionary, and set its initial count to 0
```

Content processing:

```
* Take each record line by line
* For each record
  * Convert to lowercase (can probably also do this at the word level)
  * Strip non-space punctuation
  * Split into words using space char as split token
  * For each word
    * If word exists in dictionary, increment count
```

Output generation:

```
* Sort word/count pairs in dictionary by count in descending order
* Output word and count
```

Time complexity:

- n = num words in word file
- p = num records in record file
- q = avg num words in each record in record file

- Dictionary generation: O(n)
- Parsing records and generating counts: O(p*q)
  - O(1) word lookup to increment counter
- Output generation: O(n*lg(n)) to sort by count descending and output all records
- => O(p*q) assuming the records file is going to be the predominant factor

Space complexity:

- Counting and word dictionaries: O(n) each
- => O(n)

## Initial Implementation: `count_words.py`

This Python3 program takes as optional arguments a word file and a records file, and
outputs to stdout the words and the counts, in descending order by count.

Example:

```
test1_words.txt:
Name
Detect
AI

test1_records.txt:
Detecting first names is tricky to do even with AI.
how do you say a street name is not a first name?

$ python3 count_words.py test1_words.txt test1_records.txt
Predefined Word                         Match Count
Name                                             2
AI                                               1
Detect                                           0
```

If no arguments are given, the program uses `words.txt` for the words file and
`records.txt` for the records file.

## Improvements

### Pretty-Printing Words

The initial output emitted the lowercased words used for matching along with their
counts. The sample output showed the original words and their counts, so in order
to try to match this, we need to maintain the linkage between the original
word as seen in the words file, and the word as it is used when counting in 
records.

Accordingly, in parsing the word file, an additional dictionary is created to
maintain that mapping from the lowercased word to its original form. This
dictionary is then used when emitting the results.

## Test Cases

* Test 1: Testing the sample words and records as given in the problem.
* Test 2: Testing case insensitivity, whole word matching.
* Test 3: Testing reasonably long word.
* Test 4: Testing word of 256 characters.

## Closing Comments and Improvements

If we wanted to do partial word matches, then we could employ something like a trie
or prefix tree to do so.

We could be better about generating "pretty" output by measuring the max string length
and adjusting output format accordingly, but it would probably start looking really
awkward with a mix of really long and really small input words. I chose 40 chars as
a reasonable initial value.

We count the total number of occurrences of a word throughout the corpus, so if a
word appears multiple times in a given record, then we count the word that number
of times, versus a single time for the matched record. If we just wanted the
number of records containing the specified word, then rather than maintaining absolute
counts, for each record, we would detect whether or not a word has occurred at least 
once. For all words that appeared at least once in a record, we increment its count
by 1 only.

The method `process_record()` then might look something like:

```python
def process_record(records_fn: str, word_dict: dict[str, int]) -> None:
	with open(records_fn) as f:
		for record in f:
			seen = set()
			record = clean_record(record)
			for word in record.split(' '):
				if word in word_dict:
					seen.add(word)
	        for word in seen:
				word_dict[word] += 1
```

If we only wanted the top-k words in the result set, then we can use a heap
to peel off the k words we want. Rough algorithm would look something like:

```
- emit output
  - create class to contain word and count, with custom __lt__() sort method
  - convert word_dict into list of word and count objects - O(num words in dictionary)
  - heapfiy list - O(n)
  - pull top-k words - O(k)
```

This could result in significant time savings generating the output, especially
if the number of total words is large but the number of top words we want 
is small.
