import urllib.request
import json
import datetime
from addressbook import *

def xvolume(x):
  '''
  xvolume: writes datetime and volume to .dat file every 'x' time-period (seconds) 
  '''

  xv = 0                                        # volume in time period 'x'
  vdigix = 0                                    # volume from digix marketplace
  vkryptono = 0                                 # volume to kryptono
  vkybert = 0                                   # volume to kyber
  vkyberf = 0                                   # volume from kyber
  tv = 0                                        # total volume
  tx = 0                                        # tx fees collected
  cx = 1                                        # count time periods (start at 1)
  ts = 0                                        # total supply
  di = d0                                       # start on d0

  with open(str(x) + '.dat','w') as f:         # open file for writing
    for i in reversed(range(0,lena)):
      # write to file every multiple of 'x' (seconds)
      ti = int(a[i]['timeStamp'])               # time of ith tx
      dt = ti - t0                              # seconds since t0
      print('t = ' + str(round(dt/(3600*24),2)) + ' days')
      if dt > cx*x:                             # if dt > cx multiples of x time periods
        cx = int(dt/x) + 1                      # a of x time periods passed
        di = di.strftime("%y-%m-%d %H:%M")
        f.write("%s %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %s" % (di,xv,ts,tx,tv,vdigix,vkybert,vkyberf,vkryptono,'\n'))
        di = d0 + datetime.timedelta(seconds=dt)                   # datetime of ith tx
        xv = 0                                                     # reset x volume 
      
      vi = float(a[i]['value'])*1e-9  # volume of ith tx
      print(vi)
      ato = a[i]['to']                # to of ith tx
      afrom = a[i]['from']            # from of ith tx
      
      if afrom == zeroaddr:  # if from 0x0 (minting)
        ts += vi  # Minting increases total supply
        continue  # continue: skip adding volume
      elif ato == zeroaddr:  # if to 0x0 (recasting)
        ts -= vi  # Recasting decreases total supply
        continue
      elif ato == recastfeeaddr:  # recast fee collector
        continue
      elif ato == txfeeaddr:  # tx fee collector
        tx += vi
        continue
      elif afrom == digixaddr: # digix
        vdigix += vi
      elif ato == kyberaddr:   # kyber
        vkybert += vi
      elif afrom == kyberaddr: # kyber
        vkyberf += vi
      elif ato == kryptonoaddr:  # kryptono
        vkryptono += vi
      
      # default actions:
      xv += vi                            # accumulate 'x'ly volume
      tv += vi                            # accumulate total volume
    
    di = di.strftime("%y-%m-%d %H:%M")
    f.write("%s %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %s" % (di,xv,ts,tx,tv,vdigix,vkybert,vkyberf,vkryptono,'\n'))
  return di,xv,tv,ts,tx

now = datetime.datetime.now()
currentdate = now.strftime("%y-%m-%d %H:%M")
with open('date.txt','w+') as f:
  f.write(str(currentdate))

# DGX on-chain volume
with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&page=1&offset=10000&sort=desc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7") as url:
  data = json.loads(url.read().decode())
a = data.get("result","None")
lena = len(a)
print('length a = ' + str(lena))

# print messages
print("This page updates hourly using data from the [DGX contract address (etherscan)](https://etherscan.io/token/0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf). Last updated:")
print(currentdate + ' UTC\n')

# loop over whole list of txs
hour = 3600
day  = 24*hour
week = 7*day
month = 30*day
quarter = 90*day

t0 = int(a[-1]['timeStamp'])             # time (s) of first tx (is last element of list in descending order from API)
tlast = a[0]['timeStamp']           # time (s) of last tx 
dt = int(tlast) - int(t0)                       # time between 1st and last txs
d0 = now - datetime.timedelta(seconds=dt)       # current time minus dt
di = d0

di,dv,tv,ts,tx = xvolume(day)
di,wv,tv,ts,tx = xvolume(week)
di,mv,tv,ts,tx = xvolume(month)

