#!/bin/bash

lynx -dump https://etherscan.io/ | grep -A 2 'Last Block' | grep 's)' | cut -d] -f2 | sed 's/[()s]//g'  > current.block

