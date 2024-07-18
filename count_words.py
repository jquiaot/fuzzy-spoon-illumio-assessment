import sys
import heapq

"""
Populates two dictionary data structures using words in the specified file.

The "counting dictionary" `count_dict` maintains a map from lowercased
word to count of occurrences, initialized to 0.

The "word dictionary" `word_dict` maintains a map from the lowercased
word to the original word as it appeared in the file. This is used
for pretty-printing the output.
"""
def create_dictionary(fn: str, count_dict: dict[str, int], word_dict: dict[str, str]) -> None:
    with open(fn) as f:
        for word in f:
            # remove leading/trailing whitespace, and lowercase it
            word = word.strip()
            if len(word) == 0:
                continue
            clean_word = word.lower()
            count_dict[clean_word] = 0
            word_dict[clean_word] = word

"""
Processes the records in the specified file against the specified dictionary,
counting occurrences of words in the dictionary from the records.

Word matches are whole word only.

Word matches are case-insensitive.
"""
def process_records(fn: str, d: dict[str, int]) -> None:
    with open(fn) as f:
        for record in f:
            record = clean_record(record)
            for word in record.split(' '):
                if word in d:
                    d[word] += 1

"""
Helper function to clean a record:

1. Strip leading and trailing whitespace
2. Lowercase
3. Remove punctuation
"""
def clean_record(record: str) -> str:
    record = record.strip().lower()
    record = ''.join(filter(lambda c: c.isalpha() or c.isdigit() or c.isspace(), record))
    return record

"""
Emit words and counts from the specified dictionary, descending order of counts. If
include_zeroes == True, include words with counts of 0.
"""
def emit_counts(count_dict: dict[str, int], word_dict: dict[str, str], include_zeroes: bool = True) -> None:
    words_and_counts = list(count_dict.items())
    words_and_counts.sort(reverse = True, key = lambda wc: wc[1])

    print(f"{'Predefined Word' : <40}{'Match Count' : >10}")
    for wc in words_and_counts:
        print(f"{word_dict[wc[0]] : <40}{wc[1] : >10}")

if __name__ == '__main__':
    words_fn = "words.txt"
    records_fn = "records.txt"
    if len(sys.argv) == 3:
        words_fn = sys.argv[1]
        records_fn = sys.argv[2]
    count_dict = {}
    word_dict = {}
    create_dictionary(words_fn, count_dict, word_dict)
    process_records(records_fn, count_dict)
    emit_counts(count_dict, word_dict)

# END
