import glob
from stop_words import get_stop_words


def main():
    positive_reviews = []
    number_of_positive_files = 0
    for positiveFile in glob.glob("PATH TO POSITIVE TRAIN SET FOLDER/*.txt"):
        number_of_positive_files += 1
        positive_reviews.append(positiveFile)

    negative_reviews = []
    number_of_negative_files = 0
    for negativeFile in glob.glob("PATH TO NEGATIVE TRAIN SET FOLDER/*.txt"):
        number_of_negative_files += 1
        negative_reviews.append(negativeFile)

    make_dictionaries(positive_reviews, "positiveDictionary.txt")
    make_dictionaries(negative_reviews, "negativeDictionary.txt")


def make_dictionaries(file_table, output_file_name):
    stop_words = get_stop_words('en')
    word_counter = {}
    total_words = 0
    total_words_in_dictionary = 0
    translation_table = dict.fromkeys(map(ord, '0123456789~*;{}_-%[].,"/\`:´?<>()!@#&$' + "'"), " ")
    for file in file_table:
        with open(file, 'r', encoding='UTF8') as f:
            for line in f:
                word_list = line.translate(translation_table).lower().split()
                for word in word_list:
                    total_words += 1
                    if word not in word_counter:
                        if word not in stop_words:
                            word_counter[word] = 1
                    else:
                        word_counter[word] = word_counter[word] + 1

    with open(output_file_name, 'w+', encoding="UTF8") as file:
        file.write(str(total_words) + "\n")
        for word, occurrence in word_counter.items():
            file.write(str(word) + ' ' + str(occurrence) + '\n')
            total_words_in_dictionary += 1
    print("Total unique words in dictionary: ", total_words_in_dictionary)


if __name__ == "__main__":
    main()



