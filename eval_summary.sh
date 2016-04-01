#!/bin/bash

for file in data/duc/*.original
do
    name=$(basename $file)
    name=${name%.original}
    echo -e "$(tput bold)$(tput smul)$name$(tput rmul)$(tput sgr0)"
    ./summary.py $file ${file%.original}.gold --baseline
    ./summary.py $file ${file%.original}.gold --hits -l -k
    echo ""
done

