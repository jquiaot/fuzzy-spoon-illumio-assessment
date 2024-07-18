import sys
import heapq

"""
Creates a dictionary (map/dict) using words in the specified file. The file
is expected to contain words, each separated by a newline. The words
are expected to be alphanumeric only, no spaces or punctuation.
"""
def create_dictionary(fn: str) -> dict[str, int]:
    d = {}
    with open(fn) as f:
        for word in f:
            # remove leading/trailing whitespace, and lowercase it
            d[word.strip().lower()] = 0
    return d

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
def emit_counts(d: dict[str, int], include_zeroes: bool = True) -> None:
    words_and_counts = list(d.items())
    words_and_counts.sort(reverse = True, key = lambda wc: wc[1])

    print(f"{'Predefined Word' : <40}{'Match Count' : >10}")
    for wc in words_and_counts:
        print(f"{wc[0] : <40}{wc[1] : >10}")

if __name__ == '__main__':
    words_fn = "words.txt"
    records_fn = "records.txt"
    if len(sys.argv) == 3:
        words_fn = sys.argv[1]
        records_fn = sys.argv[2]
    d = create_dictionary(words_fn)
    process_records(records_fn, d)
    emit_counts(d)
