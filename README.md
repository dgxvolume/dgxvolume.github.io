# dgxvolume.github.io

### The basic python logic and important tx types

When DGX is minted it appears from the zero-address (0x0), and when DGX is recast (redeemed for real gold) it is sent to 0x0 (null) and a 1% fee is sent to the recast fee address. Here I count the tx fees and the total supply of DGX, with the following python logic,

```python

# "a" is a data structure read from etherscan containing all the on-chain data...
zeroaddr = '0x0000000000000000000000000000000000000000'

for i in range(0,len(a)):       # loop over all txs
  vi = int(a[i]['value'])       # volume of ith tx
  ato = a[i]['to']              # to address of ith tx
  afrom = a[i]['from']          # from address of ith tx
  if afrom == zeroaddr:     # if from 0x0 (minting)
    ts += vi                    # Total supply increases
  elif ato == zeroaddr:     # if to 0x0 (recasting)
    ts -= vi                    # Total supply decreases if recasted
  elif ato == '0x26cab6888d95cf4a1b32bd37d4091aa0e29e7f68':     # recast fee collector
    pass                        # do nothing for now
  elif ato == '0x00a55973720245819ec59c716b7537dac5ed4617':     # tx fee collector
    tx += vi                    # count tx fees
  else:
    xv += vi                    # accumulate volume
```

