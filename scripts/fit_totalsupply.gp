#!/usr/bin/gnuplot

# for GNUPLOT5.0
reset
set output "fit.eps"
set term post eps color enh "Times-Bold" 24
set colorsequence default #default|podo|classic
#set grid

#set title "{/Symbol abcdefghijklmnopqrstuvwxyz   \245}"
#set ylabel "d^2{/Symbol s}/dp/d{/Symbol W} (mb/(MeV/c)/str)" 1,0
#set xlabel "K^+ Momentum (GeV/c)"

#set multiplot layout 1,1 title "" font ",18" margins 0.15,0.90,0.15,0.92 spacing 0.00,0.00
set multiplot
#margins <left>,<right>,<bottom>,<top>

unset title
#set title "CF_4^+ dissociative XAS using DD-vMCG and CAM-B3LYP/6-31G*"

#set xrange [0: 10]
show xrange
#set yrange [1: 1000]
show yrange
set border linewidth 2

# Top
#unset xlabel
#unset xtics
set mxtics
#Iet ytics 0,0.2,1
#set yrange [1.0 : 800]
set ylabel "Total Supply (DGX)"
set xlabel "Days since DGX went live"
#set label 1 "I = {/Helvetica W({/Symbol w};{/Helvetica:Bold x}(t=0))}" at graph 0.10,0.50

a=10
c=0
f(x) = a*x + c
fit f(x) 'totalsupply.dat' via a,c
set label "f(x) = a*x + c" at 150,34000
set label sprintf("a = %3.5g",a) at 150,27000
     cfit = gprintf("c = %s*10^%S",c)
     set label cfit at 150,20000

set key top left
 
LW=3.5
#set logscale y
plot "totalsupply.dat" w l dt 1 lt 7 lw LW t "Total supply",\
     f(x) w l dt 6 lt 8 lw LW t "Least Squares Fit"

unset multiplot
