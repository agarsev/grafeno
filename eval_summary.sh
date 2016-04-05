#!/bin/bash

trap "exit" INT

for file in data/duc/*.original
do
    name=$(basename $file)
    name=${name%.original}
    gold=${file%.original}.gold

    morewords=$(wc -w $file | awk '{print $1}')
    words=$(wc -w $gold | awk '{print $1}')

    echo -n "$name $morewords $words "
    ./summary.py $file $gold -q --baseline --hits -n $words | tr '\n' ' '
    timeout 2m ./summary.py $file $gold -q --clustering -n $words
    echo ""
done > 'results.csv'
