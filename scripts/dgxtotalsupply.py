import urllib.request
import json

def dgxtotalsupply():

  # DGX total supply
  with urllib.request.urlopen("https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
    data = json.loads(url.read().decode())
  amount = data.get("result","None")
  totalsupply = amount[:-9]

  return totalsupply
