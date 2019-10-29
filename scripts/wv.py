import urllib.request
import json
import datetime
from addressbook import *
import time

def xvolume(x):
  '''
  xvolume: writes datetime and volume to .dat file every 'x' time-period (seconds) 
  '''

  xv = 0                                        # volume in time period 'x'
  xfees = 0   # fees collected in time period 'x'
  vdigix = 0                                    # volume from digix marketplace
  vkyber = 0                                    # kyber volume
  vuniswap = 0                                  # uniswap volume
  locked_uniswap = 0                            # DGX locked in uniswap
  vrecast = 0    # recast volume
  tv = 0                                        # total volume
  tx = 0                                        # tx fees collected
  cx = 1                                        # count time periods (start at 1)
  ts = 0                                        # total supply
  di = d0                                       # start on d0

  with open(str(x) + '.dat','w') as f:         # open file for writing
    for i in range(0,lena):
      # write to file every multiple of 'x' (seconds)
      ti = int(a[i]['timeStamp'])               # time of ith tx
      dt = ti - t0                              # seconds since t0
      #print('t = ' + str(round(dt/(3600*24),2)) + ' days')
      if dt > cx*x:                             # if dt > cx multiples of x time periods
        cx = int(dt/x) + 1                      # a of x time periods passed
        di = di.strftime("%y-%m-%d %H:%M")
        f.write("%s %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.4f %12.2f %s" % (di,xv,ts,tx,tv,vdigix,vkyber,vuniswap,vrecast,xfees,locked_uniswap,'\n'))
        di = d0 + datetime.timedelta(seconds=dt)                   # datetime of ith tx
        xv = 0                                                     # reset x volume 
        xfees = 0
      
      vi = float(a[i]['value'])*1e-9  # volume of ith tx
      #print(vi)
      ato = a[i]['to'].lower()                # to of ith tx
      afrom = a[i]['from'].lower()            # from of ith tx
      
      if afrom == zeroaddr:  # if from 0x0 (minting)
        ts += vi  # Minting increases total supply
        continue  # continue: skip adding volume
      if ato == zeroaddr:  # if to 0x0 (recasting)
        vrecast += vi  # count recast amount
        ts -= vi  # Recasting decreases total supply
        continue
      if ato == recastfeeaddr:  # recast fee collector
        continue
      if ato == txfeeaddr:  # tx fee collector
        tx += vi
        xfees += vi
        continue
      if afrom == digixaddr: # digix
        vdigix += vi
      if ato in kyber or afrom in kyber:   # kyber
        vkyber += vi
      if afrom == uniswap:  # uniswap
        locked_uniswap -= vi
        vuniswap += vi
      if ato == uniswap:  # uniswap
        locked_uniswap += vi
        vuniswap += vi
      
      # default actions:
      xv += vi                            # accumulate 'x'ly volume
      tv += vi                            # accumulate total volume
    
    di = di.strftime("%y-%m-%d %H:%M")
    f.write("%s %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.2f %12.4f %12.2f %s" % (di,xv,ts,tx,tv,vdigix,vkyber,vuniswap,vrecast,xfees,locked_uniswap,'\n'))
  return di,xv,tv,ts,tx

now = datetime.datetime.now()
currentdate = now.strftime("%y-%m-%d %H:%M")
with open('date.txt','w+') as f:
  f.write(str(currentdate))

# DGX on-chain volume
c=0
a=[]
step=10000
lenx=step
startblock = 0
endb = 999999999
while lenx==step:
  c+=1
  print(c)
  time.sleep(0.5)	# only allowed 5 requests/s so delay a bit between calls
  address = "http://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&startblock=" + str(startblock) + "&endblock=" + str(endb) + "&sort=asc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7"
  #address = "https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=0x4f3afec4e5a3f2a6a1a411def7d7dfe50ee057bf&page=" + str(c) + "&offset=" + str(step) + "&sort=asc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7"
  print(address)
  with urllib.request.urlopen(address) as url:
    data = json.loads(url.read().decode())
    x = data.get("result","None")
    a += x		# append result from call to list
  lenx = len(x)
  lena = len(a)
  startblock = int(x[0]['blockNumber'])
  endblock = int(x[lenx-1]['blockNumber'])
  print(startblock)
  print(endblock)
  startblock = endblock + 1
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

t0 = int(a[0]['timeStamp'])             # time (s) of first tx 
tlast = a[-1]['timeStamp']           # time (s) of last tx 
dt = int(tlast) - int(t0)                       # time between 1st and last txs
d0 = now - datetime.timedelta(seconds=dt)       # current time minus dt
di = d0

di,dv,tv,ts,tx = xvolume(day)
di,wv,tv,ts,tx = xvolume(week)
di,mv,tv,ts,tx = xvolume(month)
di,qv,tv,ts,tx = xvolume(quarter)

