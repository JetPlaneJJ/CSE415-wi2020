''' Part A
CSE 415, Winter 2020, Assignment 1
Jia-Jia (Jay) Lin
'''

# Returns a boolean representing if the input is a multiple of 3.
def is_multiple_of_3(n):
    return n%3 == 0

# Returns the next prime number after the input.
def next_prime(m):
    m += 1
    while (not is_prime(m)):
        m+=1
    return m

def is_prime(n):
    if (n <= 1):
        return False
    check = 2
    while (check < n):
        if (n%check == 0):
            return False
        check += 1
    return True

# Returns a dictionary whose keys are words in a reference vocab, and
# whose values are the probability of occurence on an AI webpage
# (number of occurrences / number of words on the webpage)
import wordscraper
url = "http://courses.cs.washington.edu/courses/cse415/20wi/desc.html"
def empirical_probabilities(url):
    html_bytes=wordscraper.fetch()
    word_list = wordscraper.html_bytes_to_word_list(html_bytes)
    count_dict = wordscraper.make_word_count_dict(word_list)

    ref_counts = wordscraper.init_counts_for_ref_vocab()
    wordscraper.combine_page_counts_with_ref_counts(count_dict, ref_counts)
    l = list(ref_counts.keys())
    dic = {}
    for word in l:
        dic[word] = ref_counts[word] / sum(ref_counts.values())
    return dic
