import numpy as np
import glob
import sys
from stop_words import get_stop_words


def main():
    positive_dictionary = read_dictionary("positiveDictionary.txt")
    negative_dictionary = read_dictionary("negativeDictionary.txt")
    total_positive_words = get_total_words("positiveDictionary.txt")
    total_negative_words = get_total_words("negativeDictionary.txt")

    translation_table = dict.fromkeys(map(ord, '0123456789~*;{}_-%[].,"/\`:´?<>()!@#&$' + "'"), " ")
    stop_words = get_stop_words('en')

    for newFile in glob.glob(sys.argv[1]):
        word_counter_new = {}
        total_new_words = 0
        with open(newFile, 'r', encoding='UTF8') as f:
            for line in f:
                word_list_new = line.translate(translation_table).lower().split()
                for word in word_list_new:
                    total_new_words += 1
                    if word not in word_counter_new:
                        if word not in stop_words:
                            word_counter_new[word] = 1
                    else:
                        word_counter_new[word] = word_counter_new[word] + 1

        positive_score = count_score(total_positive_words, positive_dictionary, word_counter_new)
        negative_score = count_score(total_negative_words, negative_dictionary, word_counter_new)

        print("Positive score: ", positive_score)
        print("Negative score: ", negative_score)

        if positive_score > negative_score:
            print("This is a positive review!")
        elif positive_score < negative_score:
            print("This is a negative review!")
        else:
            print("Was not able to classify. Positive score: ", positive_score, ". Negative score: ", negative_score)


def read_dictionary(input_file):
    dictionary = {}
    with open(input_file, encoding="UTF8") as file:
        next(file)
        for lines in file:
            w, p = lines.split(" ")
            dictionary[w] = float(p)
    return dictionary


def get_total_words(input_file):
    with open(input_file, encoding="UTF8") as file:
        total_words = float(file.readline())
    return total_words


def count_score(total_words, dictionary, word_counter):
    score = 0.0
    for word in word_counter:
        if word in dictionary:
            score += np.log((dictionary[word] + 1) / total_words)
        else:
            total_words += 1
            score += np.log(1 / total_words)
    return score


if __name__ == "__main__":
    main()
