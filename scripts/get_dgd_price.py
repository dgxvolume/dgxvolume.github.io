from price_usd import price_usd

priceusd = price_usd('digixdao')

with open('dgdprice.txt','w') as f:         # open file for writing
  f.write("%3.3f" % priceusd)
