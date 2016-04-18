#!/bin/bash

trap "exit" INT

experiments=$(ls experiments/*.py | sed 's:experiments/\(.*\).py$:\1:')

echo "doc length summaryl" $experiments

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
    gold=${file%.original}.gold

    morewords=$(wc -w $file | awk '{print $1}')
    words=$(wc -w $gold | awk '{print $1}')

    echo -n "$name $morewords $words"
    for exp in $experiments
    do
        rouge_score $file $gold "-t experiments.$exp --hubratio 0.05"
    done
    echo ""
done

rm -f .candidate
