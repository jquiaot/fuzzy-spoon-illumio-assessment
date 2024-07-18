# Julius Quiaot - Illumio Technical Assessment

This repository contains the results of attempting Illumio's technical
assessment.

## Problem Statement

The problem statement, as per the email instructions (minor formatting fixes introduced):

Task 1: Description: Write a program that reads a file and finds matches
against a predefined set of words. There can be up to 10K entries in the list
of predefined words. The output of the program should look something like this:

Predefined word           Match count 
FirstName                        3500 
LastName                         2700 
Zipcode                          1601 

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

## Notes

TBD
