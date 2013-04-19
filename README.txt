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
here http://nltk.org/data.html)

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

In this section you must specify what your program writes in the
standard or file output.


-------------------------------------------------------------------------
--->FILES<---------------------------------------------------------------

This sections must include a description of any file your program reads
or writes. Include a description of where the file is located, how it
is formatted, and what its purpose is. Do not describe the files already
provided to you, such as the essays. Just describe the files you create,
if any.


-------------------------------------------------------------------------
--->TECHNIQUE<-----------------------------------------------------------

A brief explanation of how you exploited POS tagging to evaluate the essays.
Also state some patterns of errors in terms of POS tags that you found.


-------------------------------------------------------------------------
--->TODO<----------------------------------------------------------------

Write here a short list of what you plan to do/fix for the second part of
the project.
