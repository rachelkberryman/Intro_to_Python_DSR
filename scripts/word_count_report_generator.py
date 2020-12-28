import os
from collections import OrderedDict

def parse_text(file_path):
    """
    Takes a file path to a text file, opens the file, and returns the string.
    """
    poem = open(file_path, 'r')
    lines = poem.readlines()
    # combining all the lines of the file into 1 long string to check the wordcount of
    combined_string = ""
    for line in lines:
        combined_string += line
    return combined_string

def word_count(str):
    """
    Takes a string and counts number of times each word appears in the string.
    Returns dictionary of the form {word: num_occurances} in descending order
    by number of occurances.
    """
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    ordered_counts = dict(OrderedDict(sorted(counts.items(),
                                  key=lambda kv: kv[1], reverse=True)))

    return ordered_counts


def generate_report(reports_directory, filename, name, ordered_counts):
    """
    Takes name of poem and its word counts and generates and saves the report.
    """
    with open(os.path.join(reports_directory, filename), 'w') as f:
        print(f"Report for poem {name} \n",
              ordered_counts, file=f)


if __name__ == '__main__':
    # set directory where poems are
    text_directory = "/Users/rachelberryman/Desktop/DSR_Intro_to_Python/Intro_to_Python_DSR/text_files"
    reports_directory = "/Users/rachelberryman/Desktop/DSR_Intro_to_Python/Intro_to_Python_DSR/text_files/reports"
    if not os.path.exists(reports_directory):
        os.mkdir(reports_directory)
    for filename in os.listdir(text_directory):
        if filename.endswith(".txt"):
            # getting the
            name = filename.split('_')[0]
            combined_string = parse_text(os.path.join(text_directory, filename))
            ordered_counts = word_count(combined_string)
            generate_report(reports_directory, filename, name, ordered_counts)
