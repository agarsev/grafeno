#!/usr/bin/gnuplot -p

set key left top

set xlabel 'summary to original ratio'
set ylabel 'f-measure'

f1(x) = a1*x+b1
fit f1(x) 'results.csv' u ($3/$2):6 via a1, b1
f2(x) = a2*x+b2
fit f2(x) 'results.csv' u ($3/$2):9 via a2, b2
f3(x) = a3*x+b3
fit f3(x) 'results.csv' u ($3/$2):12 via a3, b3

set terminal pdf
set output 'plot.pdf'

plot 'results.csv' u ($3/$2):6 t 'baseline' ls 1, a1*x+b1 notitle ls 1, \
     'results.csv' u ($3/$2):12 t 'clustering' ls 4, a3*x+b3 notitle ls 4, \
     'results.csv' u ($3/$2):9 t 'hits' ls 3, a2*x+b2 notitle ls 3
