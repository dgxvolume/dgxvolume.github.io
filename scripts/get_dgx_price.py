from price_usd import price_usd

priceusd = price_usd('digix-gold-token')

with open('dgxprice.txt','w') as f:         # open file for writing
  f.write("%3.3f" % priceusd)
