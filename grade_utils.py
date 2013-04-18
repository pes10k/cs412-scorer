import os
import sentence_tokenizer
import word_order
import essay_utils
from cmd_utils import log


cols = ('1a', '1b', '1c', '1d', '2a', '2b', '3a')
implemented_grades = ('1a', '3a')
grades = [[float(n) for n in l.split()[1:]] for l in open(os.path.join("data/grades.txt")).readlines()[::-1][:-5]]


def correct_essay_grade(essay_index, grade_type):
    if grade_type not in cols:
        raise Exception('%s is not a valid grade category' % (grade_type),)
    return grades[essay_index][cols.index(grade_type)]


def grade_text(text, grade_type):
    if grade_type not in cols:
        raise Exception('%s is not a valid grade category' % (grade_type),)
    if grade_type == "3a":
        return grade_3a(text)
    elif grade_type == "1a":
        return grade_1a(text)


def grade_1a(text):
    sentences = sentence_tokenizer.parse(text)
    num_problems = 0
    num_sentences = 0
    for sentence in sentences:
        issues_in_sentence = word_order.issues_in_sentence(sentence)
        num_sentences += 1
        num_problems += len(issues_in_sentence)
    if num_problems in (0, 1):
        return 5
    elif num_problems == 2:
        return 4
    elif num_problems in (3, 4):
        return 3
    elif num_problems in (5, 6):
        return 2
    else:
        return 1


def grade_3a(text):
    sentences = sentence_tokenizer.parse(text)
    num_sentences = len(sentences)
    if num_sentences >= 6:
        return 5
    else:
        return max(num_sentences - 1, 1)


if __name__ == '__main__':
    import cmd_utils

    tests = cmd_utils.cmd_test()
    tests = [tests] if tests else ('1a', '3a')
    essay_index = int(cmd_utils.cmd_arg('--essay', 0)) - 1

    for test in tests:
        if essay_index >= 0:
            essay_text = "\n".join(essay_utils.essays[essay_index])
            received_grade = grade_text(essay_text, test)
            log("Expect %s score: %d" % (test, correct_essay_grade(essay_index, test)), 0)
            log("Received %s score: %d" % (test, received_grade), 0)
        else:
            print "Values for %s" % (test,)
            print "-------------"
            for i in range(0, len(essay_utils.essays)):
                essay_text = "\n".join(essay_utils.essays[i])
                received_grade = grade_text(essay_text, test)
                expected_grade = correct_essay_grade(i, test)
                diff = received_grade - expected_grade
                print " | ".join([str(s) for s in [(i + 1), expected_grade, received_grade, diff]])
            print "\n\n"
