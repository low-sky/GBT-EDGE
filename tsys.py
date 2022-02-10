#! /usr/bin/env python
#

import os
import sys

project = sys.argv[1]
#  rawdata/project must exist, as a check
#

#                  our GBTIDL procedures live in pro/
print("### Working in pro")
os.chdir('pro')


print("### writing do1.pro to set the summary")
fp = open('do1.pro','w')
fp.write('offline,"%s"\n' % project)
fp.write('summary,"%s.summary"\n' % project)
fp.write('exit\n')
fp.close()


print("### gbtidl do1.pro > do1.log")
os.system('gbtidl do1.pro > do1.log')


print("### parsing %s.summary to find the VANE scans" % project)
vanes = []
fp = open("%s.summary" % project)
lines = fp.readlines()
for line in lines:
    words = line.strip().split()
    if len(words) > 2:
        if words[1] == 'VANE':
            vanes.append(words[0])
fp.close()
nvanes = len(vanes)

print("### writing do2.pro")
fp = open('do2.pro','w')
fp.write('offline,"%s"\n' % project)
for v in vanes:
    fp.write('vanecal2,%s\n' % v)
fp.write('exit\n')
fp.close()


print("### gbtidl do2.pro > do2.log")
os.system('gbtidl do2.pro > do2.log')


print("### parsing do2.log to find the tsys lines for the %d VANES" % nvanes)
fp = open("do2.log")
lines = fp.readlines()
grab = False
tsys = []
for line in lines:
    words = line.strip().split()
    if len(words) > 2:
        if grab:
            tsys.append(line)
            grab = False
        if words[0][:4] == 'Tatm':
            grab = True
fp.close()


print("### writing %s.tsys with %d vanes" % (project,nvanes))
fp = open("%s.tsys" % project, "w")
fp.write("#  %s\n" % project)
for t in tsys:
    fp.write(t)
fp.close()





"""

Connecting to file: /home/sdfits/AGBT21B_024_02/AGBT21B_024_02.raw.vegas
Scan:    12 (IF:0 FD:9 PL:0)    Tsys:   1.00
(zenith) Opacity(113.52528,59527.096) = 0.3426
AtmTsys(113.52528,59527.096) = 80.4928
Tatm(113.52528,59527.096) = 269.2360
      12       188.04533       15.111458       161.62504       225.54843
Scan:    18 (IF:0 FD:9 PL:0)    Tsys:   1.00
(zenith) Opacity(113.52528,59527.100) = 0.3427
AtmTsys(113.52528,59527.100) = 80.3749
Tatm(113.52528,59527.100) = 269.1996
      18       190.07192       16.442001       161.41116       229.50203
Scan:    55 (IF:0 FD:9 PL:0)    Tsys:   1.00
(zenith) Opacity(113.52527,59527.119) = 0.3430
AtmTsys(113.52527,59527.119) = 80.2163
Tatm(113.52527,59527.119) = 269.0268
      55       191.17041       16.998825       162.73008       233.13705
"""
