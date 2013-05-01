#!/bin/bash
# Setup file to download and install dependencies for this package
# Author: Peter Snyder <snyderp@gmail.com>

EXISTS_MESSAGE="  - Already exists, skipping"

echo "Downloading needed libraries and packages for this package"

# First download the Malt Parser
echo "Downloading the Malt Parser"
if [ -d "contrib/malt-parser" ]
then
    echo $EXISTS_MESSAGE 
else
    curl http://www.maltparser.org/dist/maltparser-1.7.2.tar.gz > contrib/maltparser.tar.gz
    tar -xzf contrib/maltparser.tar.gz -C contrib/
    rm contrib/maltparser.tar.gz
    ln -s maltparser-1.7.2/ contrib/malt-parser
    ln -s maltparser-1.7.2.jar contrib/malt-parser/malt.jar
fi
echo "Done with the Malt Parser\n"

# Next, get the pre-trained Malt Parser data
echo "Downloading pretrained Malt Parser grammars"
if [ -f "contrib/malt-parser/engmalt.linear-1.7.mco" ]
then
     echo $EXISTS_MESSAGE
else
    curl http://www.maltparser.org/mco/english_parser/engmalt.linear-1.7.mco > contrib/malt-parser/engmalt.linear-1.7.mco
fi
echo "Done with downloading the Malt grammar\n"

echo "Next, downloading the Stanford Parser.  Might take a while..."
if [ -d "contrib/stanford-parser" ]
then
    echo $EXISTS_MESSAGE
else
    curl http://nlp.stanford.edu/software/stanford-parser-2013-04-05.zip > contrib/stanford-parser.zip 
    unzip -qq contrib/stanford-parser.zip -d contrib
    ln -s stanford-parser-2013-04-05/ contrib/stanford-parser
    rm contrib/stanford-parser.zip
fi
echo "Finished downloading parser\n"
