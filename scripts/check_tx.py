import urllib.request
import json

# DGX on-chain volume
with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&page=1&offset=999999&sort=asc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
  data = json.loads(url.read().decode())
amount = data.get("result","None")
x = 0
length = len(amount)

for i in range(0,length):
  if amount[i]['to'] == '0x0000000000000000000000000000000000000000':
    print(amount[i])

