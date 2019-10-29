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
  tv = 0                                        # total volume
  cx = 1                                        # count time periods (start at 1)
  vdigixdao = 0					# DigixDAO volume
  di = d0                                       # start on d0

  with open(str(x) + 'dgd.dat','w') as f:         # open file for writing
    for i in range(0,lena):
      # write to file every multiple of 'x' (seconds)
      ti = int(a[i]['timeStamp'])               # time of ith tx
      dt = ti - t0                              # seconds since t0
      #print('t = ' + str(round(dt/(3600*24),2)) + ' days')
      if dt > cx*x:                             # if dt > cx multiples of x time periods
        cx = int(dt/x) + 1                      # a of x time periods passed
        di = di.strftime("%y-%m-%d %H:%M")
        f.write("%s %12.2f %12.2f %12.2f %s" % (di,xv,tv,vdigixdao,'\n'))
        di = d0 + datetime.timedelta(seconds=dt)                   # datetime of ith tx
        xv = 0                                                     # reset x volume 
        xfees = 0
      
      vi = float(a[i]['value'])*1e-9  # volume of ith tx
      ato = a[i]['to'].lower()                # to of ith tx
      afrom = a[i]['from'].lower()            # from of ith tx
      
      if afrom == DigixDAO:
        vdigixdao -= vi
      if ato ==  DigixDAO:
        vdigixdao += vi
      
      # default actions:
      xv += vi                            # accumulate 'x'ly volume
      tv += vi                            # accumulate total volume
    
    di = di.strftime("%y-%m-%d %H:%M")
    f.write("%s %12.2f %12.2f %12.2f %s" % (di,xv,tv,vdigixdao,'\n'))
  return di,xv,tv

now = datetime.datetime.now()
#now = datetime.datetime.now() + datetime.timedelta(hours=8)  # Add 8 hours for Singapore time
currentdate = now.strftime("%y-%m-%d %H:%M")
with open('date.txt','w+') as f:
  f.write(str(currentdate))

# DGD on-chain volume
c=9  # the first 9 pages (90k transactions) are before DigixDAO existed
a=[]
error=0
step=10000
lenx=step
startblock = 7467276  # first DGD locked in DigxDAO
endb = 999999999
while lenx==step or error==1:
  c+=1
  print('Reading Etherscan API...')
  time.sleep(1)  # only allowed 5 requests/s so delay a bit between calls
  #address = "https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=" + DGDcontract + "&address=" + DigixDAO + "&page=1&offset=100&sort=asc&apikey=ZYSM7KSCKM133HSF8UG1BF8DR7"
  address = "https://api.etherscan.io/api?module=account&action=tokentx&contractaddress=" + DGDcontract + "&address=" + DigixDAO + "&startblock=" + str(startblock) + "&endblock=" + str(endb) + "&sort=asc&apikey=Z672TYZ9ZYSM7KSCKM133HSF8UG1BF8DR7"
  with urllib.request.urlopen(address) as url:
    data = json.loads(url.read().decode())
    x = data.get("result","None")
    try:
      print('page = ' + str(c) )
      a += x		# append result from call to list
      lenx = len(x)
      error=0
      print('length x = ' + str(lenx))
      startblock = int(x[0]['blockNumber'])
      endblock = int(x[lenx-1]['blockNumber'])
      print(startblock)
      print(endblock)
      startblock = endblock + 1
    except:
      print('API call failed: try again...')
      error=1
      c-=1
lena = len(a)
print('length a = ' + str(lena))


# print messages
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

di,dv,tv = xvolume(hour)
di,dv,tv = xvolume(day)
di,wv,tv = xvolume(week)
di,mv,tv = xvolume(month)
di,qv,tv = xvolume(quarter)

