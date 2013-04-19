project 1 for CS421 - University of Illinois at Chicago
Name1 psnyde2(at)uic.edu
Name2 netid2(at)uic.edu
-------------------------------------------------------------------------
--->SETUP<---------------------------------------------------------------

Before you can run our scorer, you'll need a python setup with nltk
installed.  This can be done by running something like the below:

    pip install nltk

The scorer also uses the Penn Treebank corpus to build up counts for an HMM,
so the penn treebank is also required.  This can be downloaded using the
built in nltk downloader (instructions provided on the nltk site,
http://nltk.org/data.html).

You'll also need a bash environment with a java environment recent
enough to run the Stanford Parser.  The parser files are included
with this project / archive.

Last, the program uses STDIN to determine what text to grade, so a unix
line environment that can do input redirection is needed.

-------------------------------------------------------------------------
--->INPUT<---------------------------------------------------------------

The essay scorer uses stdin, and accepts several command line arguments.
The entry file is called scoring_utils.py.

The simplest way to run the scorer is the below

    python scoring_utils.py --final-score < (path to file to score)

To grade an entire directory of files, the below command would work,
grading each input file one after another:

for i in `ls (path to directory)`; do p27 scoring_utils.py --final-score < $i; done

Because of the statistical models and the use on the Stanford Parser (in java,
which requires starting up the parser and reading its results in through STDIO),
the script can be very slow.  We promise it hasn't frozen!  If you'd like more
feedback on what the script is doing, you can pass the "--log [1-5]" command
for feedback.  For example:

    echo "A little logging please." | python scoring_utils.py --final-score --log 1

will produce some feedback, describing what the parser is doing, while

    echo "Lots more logging please." | python scoring_utils.py --final-score --log 5

will provide a torrent of feedback.

-------------------------------------------------------------------------
--->OUTPUT<--------------------------------------------------------------

For each piece of text / essay being evaluated, the following output is
generated (assuming no logging / verbose output is specified):

    1. The text "Grading"
    2. The string "----------"
    3. A copy of the text being graded, verbatum
    4. The string "----------"
    5. Each of the implemented tests, with the corresponding score, 1-5,
       appearing afterwards

Below is an example of output produced by the grading script:

    Grading
    ----------
    The red cat talked back
    ----------

    1a: 5
    1b: 5
    1c: Unimplemented
    3a: 1


-------------------------------------------------------------------------
--->FILES<---------------------------------------------------------------

Our project uses the following files to complete the grading:

    - README.txt
        This file

    - agreement_utils.py
        A set of python functions used for measuring if there is subject-
        verb agreement in a given piece of text

    - cache/
        A directory used to cache intermediate results used by the parser.
        All files written to this directory are in the format of pickled
        python dictionaries. These files can be deleted safely at any time
        and the program will regenerate them as needed.

    - cache_utils.py
        Python functions of generating, updating, and deleting the above
        mentioned cached files as needed

    - cmd_utils.py
        Python functions to make it easier to envoke different parts of this
        project's code / functionality through the commandline, instead of
        needing to write throwaway scripts or use the python interpreter

    - contrib/
        Third party code required by this script, but not written by us.
        Currently this only includes the Stanford Parser (since the
        other libraries used, such as nltk, python stdlib, etc, are all
        expected to be included in the user's environment)

    - data/
        - The provided essays and other project materials

    - essay_utils.py
        Python functions to read and make it easier to work with the included
        training essays.

    - grade_utils.py
        Bridge functions that handling envoking the functionality provided
        by other files and assessing them as 1-5 scores

    - hmm_utils.py
        Python code for generating HMM counts from the NLTK Penn Treebank data,
        as well as functions for evaluating the probabilities of sequences
        of POS tags against that test collection

    - scoring_utils.py
        Python code for scoring the included essays or inputed text (through
        STDIN) against different pieces of the included code's functionality,
        including specific grading criteria, splitting apart sentences, etc.
        This file is intended to be envoked from the commandline.

    - sentence_tokenizer.py
        Python code used for splitting a chunk of text into sentences,
        using lexical information (in addition to punctionation, etc.)

    - stanford_parser.py
        Python bridge for calling the Stanford Parser in java and parsing
        the results in a format that python / nltk can understand.

    - tag_utils.py
        Python code for dealing with sets of POS tags. The most important
        piece of funcitonality here is simplifying sequences of POS tags
        to account of language issues.

    - tree_utils.py
        Python functionality for dealing with nltk.tree.Tree and
        nltk.tree.ParentedTree structures representing Stanford Parser
        generated parses of sentences.

    - word_order.py
        Python code for measuring if a given set of words appear in the correct
        order (ie the 1a part of the project)


-------------------------------------------------------------------------
--->TECHNIQUE<-----------------------------------------------------------

The core part of our solution is in the sentence parser.  All of the
reasoning the program does is on the sentence level.  We do sentence parsing
using the following high level approach:

    1. Split input text on newlines
    2. For each line of text
        2.1. Split each sentence into all possible subsets of words where
             the input words wwere contiguious in the input sentence,
             each sub sentence is at least three words long, and
             where we're not considering that a line of text could include
             more than 3 sentences (for computational reasons).  For example,
             given the line of text "I went running the day is hot", we consider
             each of the following sub-sets of possible setences
                "I went running the day is very hot outside"
                "I went running" AND "the day is very hot outside"
                "I went running the" AND "day is very hot outside"
                "I went running the day" AND "is very hot outside"
                "I went running the day is" AND "very hot outside"
                "I went running" AND "the day is" AND "very hot outside"

        2.2. For each of these sets of sub sentences:
            2.2.1. Parse with the Stanford Parser
            2.2.2. Simply the returned tree (by normalizing tense,
                   singular/plural, simplying the stucture of nested senteces,
                   etc.)
            2.2.3. Collect sequences of POS tag sequences at the same level
                   in the tree
            2.2.4. Find the HMM probability of each POS tag sequence
            2.2.5. Apply some weights, favoring fewer subsentences and sentences
                   that start with personal pronouns
            2.2.6. Disqualify sentences that match some conditions (such as
                   starting or ending with a conjunction)
            2.2.7. Determine the probability of the joint parse
    3. Select the set of subsentences with the highest probability

Once we have a good measure of the individual sentences in the text to
be graded, we look for word order issues using the following strategy (for
each sentence in the text):

    1. Parse sentence in Stanford Parser
    2. Greatly simplify the given parse tree using methods like:
        - by normalizing tense, singular/plural, simplying the stucture of nested senteces
        - removing numbers that are next to a noun
        - collapsing complex parts of the parse tree (ex a S element that
          has only one child, a SBAR elment)
        - more items in the tree_utils.simplify_tree function
    3. Checking each level of the remaining, simplified parse tree to see if
       it has an unlikely POS tag ordering (ex VP->NP as children of a S tag,
       or NP->VP as children of a SINV tag).
    4. Return the number of blacklist rules the sentence violates (we flag
       nodes in the tree to make sure that the same POS tag sequence doesn't
       trigger multiple ordering errors)

For the 1b subject-verb agreement section, we use the following method to check
for agreement issues in each sentence

    1. Parse each sentence in Stanford Parser to generate POS parse tree
    2. Also generate the dependency information generated by the Stanford Parser
    3. For each 'nsubj' dependency returned
        3.1. Locate each end of the dependency in the parse tree
        3.2. If the nodes in the parse tree aren't one noun and one verb,
             search up in the tree to find the closest verb to the given nouns,
             and use that verb and the remaining noun node
        3.3. Check to see if the given noun and verbs are correct regarding
            singular / plural and 1st / 3rd person

In general, the hardest part of dealing with the given POS trees is that
the language problems make it common that the given trees are invaid productions
of a stict English grammar.  By combining heuristics for simplifying the tree
with the HMM probabilities, we were able to reason about the trees as if they
were more "correct" English.

-------------------------------------------------------------------------
--->TODO<----------------------------------------------------------------

 - The blacklist approach for word order is probably pretty fragile.  Might
   be better to used learned weights or something like that
 - Implement the missing 1c / verb tense grader
 - (Maybe) speed things up by batching requests to java / Stanford Parser,
   or move to Jython
