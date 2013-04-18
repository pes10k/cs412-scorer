import os
from sentence_tokenizer import parse_sentences, correct_line_counts
import essay_utils
from cmd_utils import log


cols = ('1a', '1b', '1c', '1d', '2a', '2b', '3a')

grades = [[float(n) for n in l.split()[1:]] for l in open(os.path.join("data/grades.txt")).readlines()[::-1][:-5]]


def correct_essay_grade(essay_index, grade_type):
    if grade_type not in cols:
        raise Exception('%s is not a valid grade category' % (grade_type),)
    return grades[essay_index][cols.index(grade_type)]


def grade_essay(essay_index, grade_type):
    if grade_type not in cols:
        raise Exception('%s is not a valid grade category' % (grade_type),)
    if grade_type == "3a":
        return grade_essay_3a(essay_index)


def grade_essay_1a(essay_index):
    essay = essay_utils.essays[essay_index]


def grade_essay_3a(essay_index):
    essay = essay_utils.essays[essay_index]
    num_sentences = sum([len(parse_sentences(line)) for line in essay])
    log("Found %d sentences, expected %d" % (num_sentences, sum(correct_line_counts[essay_index])), 1)
    if num_sentences >= 6:
        return 5
    else:
        return num_sentences - 1


if __name__ == '__main__':
    import cmd_utils
    tests = ('3a',)
    essay_index = int(cmd_utils.cmd_arg('--essay', 0)) - 1

    for test in tests:
        if essay_index >= 0:
            received_grade = grade_essay(essay_index, test)
            log("Expect %s score: %d" % (test, correct_essay_grade(essay_index, test)), 0)
            log("Received %s score: %d" % (test, received_grade), 0)
        else:
            print "Values for %s" % (test,)
            print "-------------"
            for essay_index in range(0, len(essay_utils.essays)):
                received_grade = grade_essay(essay_index, test)
                expected_grade = correct_essay_grade(essay_index, test)
                diff = received_grade - expected_grade
                print " | ".join([str(s) for s in [(essay_index + 1), expected_grade, received_grade, diff]])
            print "\n\n"
