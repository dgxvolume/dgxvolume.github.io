import urllib.request, json 

def price_usd( coin ):
  u = 'https://api.coinmarketcap.com/v1/ticker/' + coin
  with urllib.request.urlopen(u) as url:
    data = json.loads(url.read().decode())

  price_usd = float(data[0]['price_usd'])
  
  return price_usd
