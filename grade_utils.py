import os
from sentence_tokenizer import parse_sentences, correct_line_counts
import essay_utils

cols = ('1a', '1b', '1c', '1d', '2a', '2b', '3a')

grades = [[float(n) for n in l.split()[1:]] for l in open(os.path.join("data/grades.txt")).readlines()[::-1][:-5]]


def grade_essay_3a(essay_index):
    essay = essay_utils.essays[essay_index]
    num_sentences = sum([len(parse_sentences(line)) for line in essay])
    print "Found %d lines, expected %d" % (num_sentences, sum(correct_line_counts[essay_index]))
    if num_sentences >= 6:
        return 5
    else:
        return num_sentences - 1


if __name__ == '__main__':
    import cmd_utils
    essay_index = int(cmd_utils.cmd_arg('--essay', 0)) - 1
    if essay_index >= 0:
        received_grade = grade_essay_3a(essay_index)
        print "expect score: %d, Received score: %d" % (grades[essay_index][6], received_grade)
