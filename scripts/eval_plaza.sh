#!/bin/bash

trap "exit" INT

echo "doc length summaryl thesis1 thesis2 code1 code2"

rouge_score() {
    timeout 2m ./plaza_summary.py $3 $1 > .candidate
    if [ $? -ne 0 ]; then
        echo -n " 0"
    else
        echo -n " $(scripts/rouge_eval.js .candidate $2)"
    fi
}

for file in data/duc/*.original
do
    name=$(basename $file)
    name=${name%.original}
    #echo $name >&2
    gold=${file%.original}.gold

    morewords=$(wc -w $file | awk '{print $1}')
    words=$(wc -w $gold | awk '{print $1}')

    echo -n "$name $morewords $words"
    rouge_score $file $gold "--thesis --hubratio 0.1"
    rouge_score $file $gold "--thesis --hubratio 0.2"
    rouge_score $file $gold "--hubratio 0.1"
    rouge_score $file $gold "--hubratio 0.2"
    echo ""
done

rm -f .candidate