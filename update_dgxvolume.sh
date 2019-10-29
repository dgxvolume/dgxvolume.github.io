#!/bin/bash

git config --global user.name dgxvolume
git config --global user.email dgxvolume@protonmail.com
#git pull
cp /home/thomas/dgxvolume.github.io/_drafts/dgxvolume.html /home/thomas/dgxvolume.github.io/index.html
cp /home/thomas/dgxvolume.github.io/_drafts/digixdao.html /home/thomas/dgxvolume.github.io/digixdao.html
cd /home/thomas/dgxvolume.github.io/scripts 
echo "Running wv.py..."
python3 wv.py > intro.txt
echo "Done wv.py."
echo "Running get_dgx_price.py..."
python3 get_dgx_price.py
echo "Done get_dgx_price.py."
awk -vORS=, '{ print "\""$1"\"" }' 86400.dat | sed 's/,$/\n/' > dailydate.list
awk -vORS=, '{ print "\""$1"\"" }' 604800.dat | sed 's/,$/\n/' > weeklydate.list
awk -vORS=, '{ print "\""$1"\"" }' 2592000.dat | sed 's/,$/\n/' > monthlydate.list
awk -vORS=, '{ print "\""$1"\"" }' 7776000.dat | sed 's/,$/\n/' > quarterlydate.list
awk -vORS=, '{ print $4 }' 86400.dat | sed 's/,$/\n/' > ts.dat
awk -vORS=, '{ print $5 }' 86400.dat | sed 's/,$/\n/' > fees.dat
awk -vORS=, '{ print $6 }' 86400.dat | sed 's/,$/\n/' > tv.dat
awk -vORS=, '{ print $3 }' 86400.dat | sed 's/,$/\n/' > dv.dat
awk -vORS=, '{ print $11 }' 86400.dat | sed 's/,$/\n/' > dailyfees.dat
awk -vORS=, '{ print 1200*$11/($7+0.0001) }' 2592000.dat | sed 's/,$/\n/' > apr_monthly.dat
awk -vORS=, '{ print $7 }' 86400.dat | sed 's/,$/\n/' > digixv.dat
awk -vORS=, '{ print $8 }' 86400.dat | sed 's/,$/\n/' > kyberv.dat
awk -vORS=, '{ print $9 }' 86400.dat | sed 's/,$/\n/' > uniswapv.dat
awk -vORS=, '{ print $10 }' 86400.dat | sed 's/,$/\n/' > recastv.dat
awk -vORS=, '{ print $3 }' 604800.dat | sed 's/,$/\n/' > wv.dat
awk -vORS=, '{ print $3 }' 2592000.dat | sed 's/,$/\n/' > "mv.dat"
awk -vORS=, '{ print $3 }' 7776000.dat | sed 's/,$/\n/' > qv.dat

DGXPRICE=$(cat dgxprice.txt)
CURRENTDATE=$(cat date.txt)
DAILYDATE=$(cat dailydate.list)
WEEKLYDATE=$(cat weeklydate.list)
MONTHLYDATE=$(cat monthlydate.list)
QUARTERLYDATE=$(cat quarterlydate.list)
TOTALSUPPLY=$(cat ts.dat)
CURRENTSUPPLY=$(tail -n 1 2592000.dat | awk '{print $4}')
FEES=$(cat fees.dat)
APRMONTHLY=$(cat apr_monthly.dat)
CURRENTFEES=$(tail -n 1 2592000.dat | awk '{print $5}')
DGXSOLD=$(tail -n 1 2592000.dat | awk '{print $7}')
TOTALRECASTED=$(tail -n 1 2592000.dat | awk '{print $10}')
DIGIXVOLUME=$(cat digixv.dat)
KYBERVOLUME=$(cat kyberv.dat)
UNISWAPVOLUME=$(cat uniswapv.dat)
RECASTVOLUME=$(cat recastv.dat)
TOTALVOLUME=$(cat tv.dat)
DAILYVOLUME=$(cat dv.dat)
WEEKLYVOLUME=$(cat wv.dat)
MONTHLYVOLUME=$(cat mv.dat)
QUARTERLYVOLUME=$(cat qv.dat)

# simple calculations
TOTALSUPPLYUSD=$( awk "BEGIN {print ($DGXPRICE*$CURRENTSUPPLY)/1e6}" )
TOTALSUPPLYUSD=$( printf "%.2f" $TOTALSUPPLYUSD )
DGXSOLDUSD=$( awk "BEGIN {print ($DGXPRICE*$DGXSOLD)/1e6}" )
DGXSOLDUSD=$( printf "%.2f" $DGXSOLDUSD )
CURRENTFEESUSD=$( awk "BEGIN {print ($DGXPRICE*$CURRENTFEES)}" )
CURRENTFEESUSD=$( printf "%.2f" $CURRENTFEESUSD )

cd /home/thomas/dgxvolume.github.io/
sed -i "s/CURRENTDATE/$CURRENTDATE/" index.html
sed -i "s/CURRENTDATE/$CURRENTDATE/" about.html
sed -i "s/XRANGE/$DAILYDATE/g" index.html
sed -i "s/YRANGE/$TOTALSUPPLY/" index.html
sed -i "s/TOTALRECASTED/$TOTALRECASTED/" index.html
sed -i "s/TOTALSUPPLYUSD/$TOTALSUPPLYUSD/" index.html
sed -i "s/TOTALSUPPLY/$CURRENTSUPPLY/" index.html
sed -i "s/FEESCOLLECTED/$CURRENTFEES/" index.html
sed -i "s/FEESCOLLECTEDUSD/$CURRENTFEESUSD/" index.html
sed -i "s/DGXSOLDUSD/$DGXSOLDUSD/" index.html
sed -i "s/DGXSOLD/$DGXSOLD/" index.html
sed -i "s/DIGIXVRANGE/$DIGIXVOLUME/" index.html
sed -i "s/KYBERVRANGE/$KYBERVOLUME/" index.html
sed -i "s/UNISWAPVRANGE/$UNISWAPVOLUME/" index.html
sed -i "s/RECASTRANGE/$RECASTVOLUME/" index.html
sed -i "s/FEERANGE/$FEES/" index.html
sed -i "s/TVRANGE/$TOTALVOLUME/" index.html
sed -i "s/DVRANGE/$DAILYVOLUME/" index.html
sed -i "s/WEEKLYDATE/$WEEKLYDATE/" index.html
sed -i "s/WVRANGE/$WEEKLYVOLUME/" index.html
sed -i "s/MONTHLYDATE/$MONTHLYDATE/" index.html
sed -i "s/MVRANGE/$MONTHLYVOLUME/" index.html
sed -i "s/QUARTERLYDATE/$QUARTERLYDATE/" index.html
sed -i "s/QVRANGE/$QUARTERLYVOLUME/" index.html
sed -i "s/APRRANGE/$APRMONTHLY/" index.html

grep -v 'title:' /home/thomas/dgxvolume.github.io/index.html > /home/thomas/dgxvolume.github.io/dgxvolume.html

#=======================================================
# DGD in DigixDAO
cd /home/thomas/dgxvolume.github.io/scripts 
echo "Running dgdlocked.py..."
python3 dgdlocked.py
echo "Done dgdlocked.py."
echo "Running get_dgd_price.py..."
python3 get_dgd_price.py
echo "Done get_dgd_price.py."

# DGD locked in DigixDAO part
#tail -n +1537 3600dgd.dat > tmp  # I know that the first n transactions are not to DigixDAO
cp 3600dgd.dat tmp  
#tail -n +18893 3600dgd.dat > tmp  # I know that the first n transactions are not to DigixDAO
awk -vORS=, '{ print "\""$1 " " $2"\"" }' tmp | sed 's/,$/\n/' > dgddailydate.list
awk -vORS=, '{ print $5 }' tmp | sed 's/,$/\n/' > dgdindao.dat
DGDDATE=$(cat dgddailydate.list)
DGDINDAO=$(cat dgdindao.dat)
DGDTOTALINDAO=$(tail -n 1 2592000dgd.dat | awk '{print $5}')
DGDPRICE=$(cat dgdprice.txt)

CURRENTDATE=$(cat date.txt)

# simple calculations
DGDTOTALINDAOUSD=$( awk "BEGIN {print ($DGDPRICE*$DGDTOTALINDAO)/1e6}" )
DGDTOTALINDAOUSD=$( printf "%.2f" $DGDTOTALINDAOUSD )
DGDPCOFTOTALSUPPLY=$( awk "BEGIN {print (100*$DGDTOTALINDAO/2e6)}" )
DGDPCOFTOTALSUPPLY=$( printf "%.2f" $DGDPCOFTOTALSUPPLY )

cd /home/thomas/dgxvolume.github.io/
sed -i "s/CURRENTDATE/$CURRENTDATE/" digixdao.html
sed -i "s/DGDDATE/$DGDDATE/" digixdao.html
sed -i "s/DGDINDAO/$DGDINDAO/" digixdao.html
sed -i "s/DGDTOTALINDAO/$DGDTOTALINDAO/" digixdao.html
sed -i "s/DGDTOTALINDAOUSD/$DGDTOTALINDAOUSD/" digixdao.html
sed -i "s/DGDPCOFTOTALSUPPLY/$DGDPCOFTOTALSUPPLY/" digixdao.html
#=======================================================

git checkout --orphan newBranch
git add -A  # Add all files and commit them
git commit -m 'reset git'
git branch -D master  # Deletes the master branch
git branch -m master  # Rename the current branch to master
git branch -D newBranch  # Deletes the other branch
git push -f origin master  # Force push master branch to github
git gc --aggressive --prune=all     # remove the old files

